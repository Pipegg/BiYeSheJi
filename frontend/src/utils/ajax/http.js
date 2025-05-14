import axios from "axios";
import config from "@/config";
import Qs from "qs";
import jdk, { isArray } from "@/utils/extend";
import router from "@/router";
import { useUserStore } from "@/stores";
import { ElMessage } from "element-plus";

// 添加获取 CSRF token 的函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 添加调试工具函数
function debugRequest(config, label = '请求配置') {
    // 特殊处理学习和聊天相关API的调试信息
    const isLearningOrChatApi = config.url && (
        config.url.includes('/api/ai/learning') || 
        config.url.includes('/api/chat/')
    );
    
    if (isLearningOrChatApi) {
        console.log(`DEBUG ${label} [${config.method?.toUpperCase() || 'GET'}] ${config.url}:`, {
            headers: { ...config.headers },
            params: config.params ? { ...config.params } : undefined,
            data: config.data ? (typeof config.data === 'object' ? { ...config.data } : config.data) : undefined,
            auth: {
                hasToken: !!(config.headers?.token || config.headers?.Authorization),
                hasUserId: !!(
                    (config.params && config.params.user_id) || 
                    (config.data && config.data.user_id)
                ),
                hasRole: !!(
                    (config.params && config.params.role) || 
                    (config.data && config.data.role)
                ),
            }
        });
    }
}

// 创建axios实例
var https = axios.create({
    baseURL: config.service_url,
    withCredentials: true,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },
    // 添加请求转换器，确保所有POST请求的数据被正确序列化
    transformRequest: [function (data, headers) {
        if (data && headers['Content-Type'] && headers['Content-Type'].includes('application/json')) {
            try {
                // 添加调试输出(安全打印)
                const sanitizedData = typeof data === 'object' ? { ...data } : data;
                console.log('transformRequest - 处理前数据类型:', typeof data, 
                           'isArray:', Array.isArray(data), 
                           '数据:', sanitizedData);
                           
                // 确保对象可以被序列化
                const serializedData = JSON.stringify(data);
                console.log('transformRequest - 序列化后长度:', serializedData.length);
                return serializedData;
            } catch (e) {
                console.error('数据序列化错误:', e);
                // 返回空对象作为兜底
                return JSON.stringify({});
            }
        }
        return data;
    }],
    // 添加响应转换器，标准化响应格式
    transformResponse: [function(data) {
        try {
            // 尝试将响应解析为JSON
            const parsedData = JSON.parse(data);
            
            // 处理嵌套数据结构的检测
            if (typeof parsedData === 'object' && parsedData !== null) {
                // 检查是否存在嵌套数据结构，常见格式为 {code: 0, msg: '', data: {data: [...]}}
                if (parsedData.code === 0 && parsedData.data && 
                    typeof parsedData.data === 'object' && 'data' in parsedData.data) {
                    // 学习分析API特殊处理
                    const isLearningAnalysisAPI = parsedData.api_path && 
                        parsedData.api_path.includes('/api/ai/learning-analysis');
                    
                    console.log('找到嵌套数据结构, 返回 response.data.data:', parsedData.data.data);
                    
                    // 为学习分析API进行特殊处理 - 自动解包嵌套数据
                    if (isLearningAnalysisAPI) {
                        console.log('为学习分析API自动解包嵌套数据');
                        
                        // 保留原始的 metadata (total, page, limit)
                        const metadata = {
                            total: parsedData.data.total,
                            page: parsedData.data.page,
                            limit: parsedData.data.limit
                        };
                        
                        // 将嵌套数据提升到顶层
                        parsedData.originalData = parsedData.data;
                        parsedData.data = parsedData.data.data;
                        
                        // 保留元数据
                        parsedData.metadata = metadata;
                    }
                }
                
                // 为学习分析和聊天API添加更详细的日志
                const isLearningOrChatApi = parsedData.api_path && (
                    parsedData.api_path?.includes('/api/ai/learning') ||
                    parsedData.api_path?.includes('/api/chat/')
                );
                
                if (isLearningOrChatApi) {
                    console.log('API响应数据结构:', {
                        statusCode: parsedData.code,
                        hasData: !!parsedData.data,
                        dataType: parsedData.data ? typeof parsedData.data : null,
                        message: parsedData.msg || ''
                    });
                }
            }
            return parsedData;
        } catch (e) {
            // 解析失败则返回原始数据
            console.warn('响应解析失败:', e);
            return data;
        }
    }]
});

// 创建AI服务专用的axios实例
const aiHttps = axios.create({
    baseURL: config.service_url,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
});

// 添加AI服务请求拦截器
aiHttps.interceptors.request.use(
    config => {
        // 从store获取最新token
        const userStore = useUserStore();
        
        // 添加token到请求头和参数中，确保认证正常工作
        if (userStore.token) {
            // 添加token到请求头
            config.headers['token'] = userStore.token;
            config.headers['Authorization'] = `Bearer ${userStore.token}`;
            
            // 对于GET请求，添加token到URL参数
            if (config.method === 'get') {
                config.params = {
                    ...(config.params || {}),
                    token: userStore.token
                };
            }
            
            // 对于POST请求，确保也在数据中包含token（某些后端实现可能从请求体获取token）
            if (config.method === 'post' && config.data) {
                if (typeof config.data === 'string') {
                    try {
                        const dataObj = JSON.parse(config.data);
                        dataObj.token = userStore.token;
                        config.data = JSON.stringify(dataObj);
                    } catch(e) {
                        // 如果不是JSON字符串，保持原样
                        console.warn('无法解析POST数据为JSON', e);
                    }
                } else if (typeof config.data === 'object') {
                    // 如果是对象，直接添加token
                    config.data.token = userStore.token;
                }
            }
        }
        
        // 启用跨域凭证
        config.withCredentials = true;
        
        console.log(`AI请求: ${config.method} ${config.url} - 带认证: ${!!userStore.token}`, config.headers);
        return config;
    },
    error => {
        console.error('AI请求拦截器错误:', error);
        return Promise.reject(error);
    }
);

// 添加AI服务响应拦截器
aiHttps.interceptors.response.use(
    response => {
        console.log(`AI响应: ${response.config.method} ${response.config.url} - 状态: ${response.status}`);
        
        // 检查响应是否包含数据
        if (!response.data) {
            console.warn('AI响应没有数据:', response);
            return null;
        }
        
        // 直接返回数据部分，简化处理
        return response.data;
    },
    error => {
        // 详细记录错误信息以便调试
        console.error('AI请求失败:', {
            url: error.config?.url,
            method: error.config?.method,
            status: error.response?.status,
            statusText: error.response?.statusText,
            headers: error.config?.headers,
            message: error.message
        });
        
        // 特殊处理学习路径和AI相关错误
        if (error.response) {
            const status = error.response.status;
            const url = error.config.url;
            
            // 特殊处理学习路径路由
            if (url.includes('/api/ai/learning-path')) {
                if (status === 403 || status === 401) {
                    console.warn('学习路径API访问需要认证 - 返回特殊错误');
                    
                    // 增强认证信息检查
                    const userStore = useUserStore();
                    if (userStore.isLogin()) {
                        console.log('用户登录状态检查通过但API访问仍被拒绝 - 可能是会话问题');
                        
                        // 检查响应体中的具体错误信息
                        let errorMsg = '请先登录后再访问学习路径';
                        let isAuthError = true;
                        try {
                            if (error.response.data && error.response.data.msg) {
                                errorMsg = error.response.data.msg;
                                isAuthError = !!error.response.data.auth_error; // 明确指定为认证错误
                            }
                        } catch (e) {
                            // 解析错误时使用默认消息
                        }
                        
                        // 创建特殊错误对象，标记为认证错误
                        const authError = new Error(errorMsg);
                        authError.authError = isAuthError;
                        authError.response = error.response;
                        authError.originalError = error;
                        authError.userState = {
                            hasToken: !!userStore.token,
                            hasSession: !!userStore.session && typeof userStore.session === 'object',
                            loggedIn: userStore.isLogin()
                        };
                        
                        return Promise.reject(authError);
                    } 
                }
            }
        }
        
        return Promise.reject(error);
    }
);

// 请求拦截器
axios.interceptors.request.use(
    config => {
        const userStore = useUserStore();

        // 记录请求详情
        console.log(`发送请求: ${config.method?.toUpperCase() || 'GET'} ${config.url}`);
        
        // 特殊处理学习分析API
        const isLearningAnalysisAPI = config.url && (
            config.url.includes('/api/ai/learning') || 
            config.url.includes('/learning-analysis')
        );
        
        // 除非特别要求，始终添加token到请求头
        if (userStore.token) {
            config.headers = config.headers || {};
            config.headers['token'] = userStore.token;
            config.headers['Authorization'] = `Bearer ${userStore.token}`;

            // 特别处理学习分析API，确保令牌在URL参数中也存在
            if (isLearningAnalysisAPI && config.method?.toLowerCase() === 'get') {
                config.params = config.params || {};
                if (!config.params.token) {
                    config.params.token = userStore.token;
                }
                
                // 确保用户ID和角色也被添加到参数中
                if (userStore.session) {
                    if (userStore.session.username && !config.params.user_id) {
                        config.params.user_id = userStore.session.username;
                    }
                    if (!config.params.role) {
                        config.params.role = 'student';
                    }
                    if (userStore.session.cx && !config.params.cx) {
                        config.params.cx = userStore.session.cx;
                    }
                    if (userStore.session.table && !config.params.table) {
                        config.params.table = userStore.session.table;
                    }
                    if (userStore.session.id && !config.params.id) {
                        config.params.id = userStore.session.id;
                    }
                }
            }
        }
        
        // 为API请求启用凭证
        const isApiRequest = config.url && (
            config.url.includes('/api/') || 
            config.url.includes('tokenLogin') || 
            config.url.includes('login/')
        );
        
        if (isApiRequest) {
            config.withCredentials = true;
        }
        
        // 添加时间戳防止缓存（GET请求）
        if (config.method === 'get') {
            config.params = {
                ...config.params,
                _t: Date.now()
            };
        }
        
        // 优化学习分析和智能问答API的参数处理
        const isLearningOrChatApi = config.url && (
            config.url.includes('/api/ai/learning') || 
            config.url.includes('/api/chat/')
        );
        
        if (isLearningOrChatApi) {
            // 使用调试日志记录请求详情
            debugRequest(config, '请求拦截器');
            
            // 确保参数被直接传递，避免 headers 和 params 对象被序列化为字符串
            if (config.params && typeof config.params === 'object') {
                // 确保角色信息被正确传递
                if (!config.params.role && config.method === 'get') {
                    config.params.role = 'student';  // 默认角色
                }
                
                // 检查 params 是否已经包含了不正确的参数
                if (config.params.headers || config.params.params) {
                    console.warn('检测到params对象内嵌了headers或params属性，这可能导致错误。正在修正...');
                    
                    // 创建新的params对象，过滤掉嵌套的headers和params
                    const cleanParams = {};
                    Object.keys(config.params).forEach(key => {
                        if (key !== 'headers' && key !== 'params') {
                            cleanParams[key] = config.params[key];
                        } else {
                            // 将嵌套对象中的属性提升到顶层
                            const nestedObj = config.params[key];
                            if (nestedObj && typeof nestedObj === 'object') {
                                Object.keys(nestedObj).forEach(nestedKey => {
                                    cleanParams[nestedKey] = nestedObj[nestedKey];
                                });
                            }
                        }
                    });
                    
                    // 更新配置中的params
                    config.params = cleanParams;
                    console.log('修正后的params对象:', config.params);
                }
            }
        }
        
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 添加响应拦截器
https.interceptors.response.use(
    response => {
        // 保存原始URL和方法用于调试
        const requestUrl = response.config.url;
        const requestMethod = response.config.method;
        const userStore = useUserStore();
        
        console.log(`响应拦截(${requestMethod}): ${requestUrl} - 状态: ${response.status}`);
        
        // 验证码请求特殊处理
        if (requestUrl.includes('captch')) {
            // 验证码请求不进行任何处理，直接返回原始数据
            if (response.data) {
                return response.data;
            }
        }
        
        // 退出登录请求特殊处理
        if (requestUrl.includes('/logout')) {
            console.log('退出登录响应处理:', response.data);
            // 确保登出请求总是成功，即使后端出错
            return {
                code: 0,
                msg: '退出成功',
                data: null
            };
        }
        
        // 登录请求特殊处理
        if (requestUrl.includes('/login')) {
            console.log('登录响应处理:', response.data);
            
            // 确保登录成功响应包含有效的 session 和 token
            if (response.data && response.data.code === 0 && response.data.data) {
                const loginData = response.data.data;
                // 检查 session 对象格式
                if (!loginData.session || !loginData.token) {
                    console.error('登录响应缺少关键数据:', loginData);
                    // 尝试直接响应中获取 session 和 token
                    if (response.data.session && response.data.token) {
                        console.log('从响应根节点提取session和token');
                        // 使用根节点的session和token
                        userStore.setToken(response.data.token);
                        userStore.setSession(response.data.session);
                    }
                }
            }
            
            // 登录请求直接返回 data 部分，不做额外处理
            if (response.data) {
                return response.data;
            }
        }
        
        // AI API 路径处理
        if (requestUrl.includes('/api/ai/')) {
            // AI API 请求直接返回 data 部分
            if (response.data) {
                return response.data;
            }
        }
        
        // token登录请求特殊处理
        if (requestUrl.includes('/tokenLogin')) {
            console.log('Token登录响应处理:', response.data);
            
            // 首先检查返回格式
            const rawData = response.data;
            
            // 直接返回原始数据，由业务代码处理
            if (rawData) {
                // 尝试提取session和token
                if (rawData.session && rawData.token) {
                    // 非标准格式但有效的直接响应
                    console.log('Token登录直接返回会话:', {
                        username: rawData.session.username,
                        hasToken: !!rawData.token
                    });
                    return rawData;
                }
                
                // 标准格式code/data结构
                if (rawData.code === 0 && rawData.data) {
                    // 标准响应格式
                    console.log('Token登录标准响应:', {
                        hasSession: !!rawData.data.session,
                        hasToken: !!rawData.data.token
                    });
                    return rawData;
                }
                
                // 兜底处理 - 原样返回
                return rawData;
            }
        }
        
        // 检查响应数据是否为空
        if (!response.data) {
            console.error('响应数据为空:', requestUrl);
            return Promise.reject(new Error('响应数据为空'));
        }
        
        // 常规响应处理
        const data = response.data;
        if (data.code === 0) {
            return data;
        } else if (data.code === 401 || data.code === 403) {
            console.warn('认证错误:', data.msg);
            
            // 检查是否是不需要自动登出的特殊请求
            const skipAutoLogout = [
                '/api/ai/learning-path', 
                '/api/chat',
                '/api/ai/'
            ].some(path => requestUrl.includes(path));
            
            if (!skipAutoLogout) {
                // 清除认证信息并跳转登录页
                userStore.setToken(null);
                userStore.setSession(null);
                userStore.setRoles(null);
                
                router.replace({
                    path: "/login",
                    query: { callback: router.currentRoute.value.fullPath }
                });
            } else {
                // 对于跳过自动登出的特殊路径，尝试刷新token然后重试请求
                console.log('特殊路径，尝试刷新token后重试:', requestUrl);
                
                // 使用闭包存储原始配置以允许重试
                const originalConfig = response.config;
                
                // 如果配置中已经标记为重试，则不再尝试
                if (originalConfig._retry) {
                    console.log('请求已经重试过，不再尝试');
                    return Promise.reject(new Error(data.msg || '未授权访问'));
                }
                
                // 标记为重试以防无限循环
                originalConfig._retry = true;
                
                // 尝试使用token登录刷新会话
                return userStore.tokenLogin()
                    .then(loginResult => {
                        console.log('Token刷新结果:', loginResult);
                        
                        if (loginResult && (loginResult.code === 0 || loginResult.token)) {
                            console.log('Token刷新成功，重试请求');
                            
                            // 更新请求配置中的token
                            const token = userStore.token;
                            if (token) {
                                originalConfig.headers = originalConfig.headers || {};
                                originalConfig.headers.token = token;
                                originalConfig.headers.Authorization = `Bearer ${token}`;
                            }
                            
                            // 确保携带cookie
                            originalConfig.withCredentials = true;
                            
                            // 重试原始请求
                            return axios(originalConfig);
                        } else {
                            console.warn('Token刷新失败，放弃重试');
                            return Promise.reject(new Error(data.msg || '未授权访问'));
                        }
                    })
                    .catch(error => {
                        console.error('Token刷新出错:', error);
                        return Promise.reject(new Error(data.msg || '未授权访问'));
                    });
            }
            
            return Promise.reject(new Error(data.msg || '未授权访问'));
        } else {
            // 仅对非静默请求显示错误消息
            const isSilent = response.config.headers?._skipErrorMessage === true;
            if (!isSilent) {
                ElMessage.error(data.msg || '请求失败');
            }
            
            return Promise.reject(new Error(data.msg || '请求失败'));
        }
    },
    error => {
        // 网络错误或服务器错误处理
        const requestConfig = error.config || {};
        const requestUrl = requestConfig.url || 'unknown';
        const isSilent = requestConfig.headers?._skipErrorMessage === true;
        const userStore = useUserStore();
        
        console.error(`请求错误: ${requestUrl}`, error);
        
        if (error.response) {
            const status = error.response.status;
            
            // 检查是否处理特殊路径
            const isSpecialPath = [
                '/api/ai/learning-path',
                '/api/chat'
            ].some(path => requestUrl.includes(path));
            
            switch (status) {
                case 401:
                    // 未授权
                    if (!isSpecialPath && !isSilent) {
                        // 清除用户信息
                        userStore.setToken(null);
                        userStore.setSession(null);
                        userStore.setRoles(null);
                        
                        // 重定向到登录页面
                        router.replace({
                            path: "/login",
                            query: { callback: router.currentRoute.value.fullPath }
                        });
                        
                        if (!isSilent) {
                            ElMessage.error('您的登录已过期，请重新登录');
                        }
                    }
                    break;
                    
                case 403:
                    if (!isSpecialPath && !isSilent) {
                        ElMessage.error('您没有权限访问该资源');
                    }
                    break;
                    
                case 404:
                    if (!isSilent) {
                        ElMessage.error('请求的资源不存在');
                    }
                    break;
                    
                case 500:
                    if (!isSilent) {
                        ElMessage.error('服务器内部错误');
                    }
                    break;
                    
                default:
                    if (!isSilent) {
                        ElMessage.error(`网络错误(${status})`);
                    }
            }
        } else if (error.request) {
            // 请求已发送但未收到响应
            if (!isSilent) {
                ElMessage.error('服务器无响应，请检查网络连接');
            }
        } else {
            // 请求配置错误
            if (!isSilent) {
                ElMessage.error('请求配置错误: ' + error.message);
            }
        }
        
        return Promise.reject(error);
    }
);

function fetchModel(url, content) {
    if (!(this instanceof fetchModel)) {
        return new fetchModel(url, content);
    }
    var userStore = useUserStore();

    this._content = content;
    this._init = jdk.extend(true, {}, {
        method: "GET",
        cache: "no-cache",
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            token: userStore.token,
        },
        cors: "cors",
        credentials: true,
        data: null,
    });
    
    if (content) {
        this.body(content);
    }
    
    this.url(url);
    this.json();
}

fetchModel.baseUrl = config.service_url;

fetchModel.prototype = {
    _url: "",
    _content: null,
    _init: null,
    _leval: false,

    method: function (method) {
        this._init.method = method;
        return this;
    },
    get: function () {
        return this.method("GET");
    },
    post: function () {
        return this.method("POST");
    },
    json() {
        return this.header("Content-Type", "application/json;charset=UTF-8");
    },
    url: function (url) {
        this._url = url;
        return this;
    },
    header: function (name, value) {
        this._init.headers[name] = value;
        return this;
    },
    body: function (value) {
        this._init.data = value;
        return this;
    },
    then: function (fn, fn2) {
        var url = this.getUrl();
        return new Promise((resolve, reject) => {
            // 完全重写请求配置
            let axiosConfig = {
                url: url,
                method: this._init.method,
                headers: this._init.headers,
                timeout: 30000,
                withCredentials: true
            };
            
            // 根据请求类型设置数据
            if (this._init.method === 'POST') {
                if (this._init.data) {
                    // 将数据作为请求体发送
                    axiosConfig.data = this._init.data;
                }
            } else if (this._init.method === 'GET') {
                if (this._init.data) {
                    // GET 请求使用 params
                    axiosConfig.params = this._init.data;
                }
            }
            
            https(axiosConfig)
                .then((result) => {
                    var data = result && result.data ? result.data : result;
                    resolve(data);
                })
                .catch(reject);
        }).then(fn, fn2);
    },
    getUrl: function() {
        var url = this._url;
        if (this._init.method == "GET" && this._init.data) {
            var body = this._init.data;
            // 添加调试输出
            console.log('fetchModel.getUrl - 原始URL:', url);
            console.log('fetchModel.getUrl - 参数对象:', body);
            
            if (jdk.isObject(body)) {
                var queryParts = [];
                
                // 检查是否有嵌套的params或headers对象
                if (body.params || body.headers) {
                    console.warn('fetchModel.getUrl - 检测到嵌套的params或headers对象，正在修正...');
                    const flattenedBody = {};
                    
                    // 复制除params和headers之外的所有字段
                    Object.keys(body).forEach(key => {
                        if (key !== 'params' && key !== 'headers') {
                            flattenedBody[key] = body[key];
                        }
                    });
                    
                    // 如果存在params对象，将其字段添加到顶层
                    if (body.params && typeof body.params === 'object') {
                        Object.keys(body.params).forEach(key => {
                            flattenedBody[key] = body.params[key];
                        });
                    }
                    
                    body = flattenedBody;
                    console.log('fetchModel.getUrl - 修正后的参数对象:', body);
                }
                
                // 处理参数
                for (var key in body) {
                    if (body.hasOwnProperty(key)) {
                        // 确保参数值不是undefined或null
                        const paramValue = body[key] !== undefined && body[key] !== null ? body[key] : '';
                        
                        // 对对象类型参数进行特殊处理
                        if (typeof paramValue === 'object' && paramValue !== null) {
                            console.warn(`fetchModel.getUrl - 参数 '${key}' 是对象类型，将进行JSON序列化`);
                            const jsonValue = JSON.stringify(paramValue);
                            queryParts.push(encodeURIComponent(key) + '=' + encodeURIComponent(jsonValue));
                        } else {
                            queryParts.push(encodeURIComponent(key) + '=' + encodeURIComponent(paramValue));
                        }
                    }
                }
                var query = queryParts.join('&');
                url += (url.indexOf("?") == -1 ? "?" : "&") + query;
            } else {
                url += (url.indexOf("?") == -1 ? "?" : "&") + body;
            }
            this._init.data = null;
            console.log('fetchModel.getUrl - 最终URL:', url);
        }
        return url;
    }
};

export function fetchGet(url, param) {
    var m = new fetchModel(url).get();
    if (param) m.body(param);
    return m;
}

export function fetchPost(url, param) {
    var m = new fetchModel(url).post();
    if (param) {
        console.log('fetchPost 参数:', param);
        m.body(param);
    }
    
    // 如果是登录请求，增加特殊处理
    if (url.includes('/login')) {
        return m.then((res) => {
            console.log('fetchPost login response before processing:', res);
            return res;
        });
    }
    
    return m;
}

export function fetchPostJson(url, param) {
    console.log('fetchPostJson 发送请求到:', url);
    console.log('fetchPostJson 参数:', param);
    
    // 确保参数是对象并且可序列化
    let safeParam = param;
    
    // 检查参数是否是代理对象 - 使用更安全的方式
    try {
        // 看是否有 toJSON 方法或者是否可以安全地序列化
        if (param && typeof param === 'object') {
            safeParam = JSON.parse(JSON.stringify(param));
            console.log('安全转换对象:', safeParam);
        }
    } catch (e) {
        console.error('转换对象失败:', e);
        // 回退到原始对象
        safeParam = param;
    }
    
    // 直接使用 axios 发送请求
    return https({
        method: 'POST',
        url: url,
        data: safeParam,
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(response => {
        console.log('fetchPostJson 响应:', response);
        return response.data;
    }).catch(error => {
        console.error('fetchPostJson 错误:', error);
        return Promise.reject(error);
    });
}

// 添加代理函数处理第三方请求
export function createProxyRequest(externalUrl) {
    // 将第三方请求转发到自己的后端代理接口
    return fetchPost('/api/proxy', {
        target_url: externalUrl,
    }).then(response => {
        console.log('Proxy response:', response);
        return response;
    }).catch(error => {
        console.error('Proxy request failed:', error);
        return Promise.reject(error);
    });
}

/**
 * 检测并处理可能的CORS问题
 * 如果URL包含第三方域名如aitopia.ai，则自动通过代理发送请求
 */
export function safeFetch(url, options = {}) {
    if (url.includes('://') && !url.includes(config.service_url)) {
        return createProxyRequest(url);
    }
    return fetchModel(url, options);
}

// 导出AI HTTP实例
export const aiHttp = aiHttps;

// 扩展默认导出，包含AI HTTP实例
export default {
    http: fetchModel,
    get: fetchGet,
    post: fetchPost,
    json: fetchPostJson,
    safeFetch,
    createProxyRequest,
    aiHttp // 添加AI HTTP实例
};
