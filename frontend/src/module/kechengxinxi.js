import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

/**
 * 响应式的对象数据
 */

export const KechengxinxiCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        kechengbianhao: rule.getID(),
        kechengmingcheng: "",
        kechengfenlei: "",
        kechengfengmian: "",
        kechengyaodian: "",
        fabujiaoshi: $session.username,
        kechengxiangqing: "",

        issh: "否",
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canKechengxinxiCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = KechengxinxiCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取课程信息 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useKechengxinxiCreateForm = () => {
    const form = KechengxinxiCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canKechengxinxiSelect = (filter, result) => {
    http.post("/kechengxinxi/index/").then((res) => {
        if (res.code == 0) {
            extend(result, res.data);
        } else {
            ElMessageBox.alert(res.msg);
        }
    });
};

/**
 * 获取分页数据
 * @param filter
 */
export const useKechengxinxiSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canKechengxinxiSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canKechengxinxiFindById = (id) => {
    return new Promise((resolve, reject) => {
        console.log(`Fetching kechengxinxi with ID: ${id}`, typeof id);
        
        // 验证ID参数
        if (id === undefined || id === null) {
            console.error('无效的ID参数: undefined/null');
            return reject(new Error('无效的课程ID参数'));
        }
        
        // 确保ID是数字类型
        let numericId = id;
        if (typeof id !== 'number') {
            numericId = parseInt(id, 10);
            if (isNaN(numericId)) {
                console.error('ID参数无法转换为数字:', id);
                return reject(new Error('课程ID必须是数字'));
            }
            console.log('ID已转换为数字:', numericId);
        }
        
        // 添加认证状态检查
        const userStore = useUserStore();
        console.log('认证状态:', {
            hasToken: !!userStore.token,
            isLoggedIn: userStore.isLogin(),
            sessionExists: !!userStore.session
        });
        
        // 导入config
        import('@/config').then(configModule => {
            const config = configModule.default;
            
            // 构建请求URL
            const requestUrl = `${config.service_url}/kechengxinxi/findById/?id=${numericId}`;
            console.log('请求URL:', requestUrl);
            
            // 使用原生fetch请求
            fetch(requestUrl, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${userStore.token}`,
                    'token': userStore.token,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include' // 确保包含cookie
            })
            .then(response => {
                console.log('收到原始响应:', response.status, response.statusText);
                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('解析后的响应数据:', data);
                
                if (data && data.code === 0 && data.data) {
                    console.log('请求成功，返回数据:', data.data);
                    
                    // 尝试使用localStorage缓存数据
                    try {
                        if (data.data && data.data.id) {
                            const cacheKey = `kechengxinxi_${data.data.id}`;
                            localStorage.setItem(cacheKey, JSON.stringify(data.data));
                            console.log('数据已缓存到localStorage:', cacheKey);
                        }
                    } catch (cacheError) {
                        console.warn('缓存数据失败:', cacheError);
                    }
                    
                    resolve(data.data);
                } else {
                    console.error('响应格式不符合预期:', data);
                    throw new Error(data.msg || '服务器返回了一个无效的响应格式');
                }
            })
            .catch(error => {
                console.error('请求或解析过程中出错:', error);
                
                // 尝试从本地缓存获取数据
                try {
                    const cacheKey = `kechengxinxi_${numericId}`;
                    const cachedData = localStorage.getItem(cacheKey);
                    
                    if (cachedData) {
                        console.log('从localStorage获取缓存数据:', cacheKey);
                        const parsedData = JSON.parse(cachedData);
                        resolve(parsedData);
                        return;
                    }
                } catch (cacheError) {
                    console.warn('从缓存获取数据失败:', cacheError);
                }
                
                // 尝试从本地数据库获取数据
                import('@/utils/db').then(dbModule => {
                    const DB = dbModule.default;
                    console.log('尝试从本地数据库获取数据:', numericId);
                    
                    DB.name("kechengxinxi").where("id", numericId).find()
                        .then(localData => {
                            if (localData && Object.keys(localData).length > 0) {
                                console.log('从本地获取数据成功:', localData);
                                resolve(localData);
                            } else {
                                console.warn('本地数据库中没有数据');
                                reject(new Error('获取课程信息失败，请稍后再试'));
                            }
                        })
                        .catch(dbError => {
                            console.error('从本地数据库获取数据失败:', dbError);
                            reject(new Error('获取课程信息失败，请稍后再试'));
                        });
                }).catch(importError => {
                    console.error('导入DB模块失败:', importError);
                    reject(new Error('获取课程信息失败，请稍后再试'));
                });
            });
        }).catch(importError => {
            console.error('导入config模块失败:', importError);
            reject(new Error('加载配置失败，请刷新页面重试'));
        });
    });
};

/**
 * 根据id 获取一行数据
 * @param id
 * @return {UnwrapNestedRefs<{}>}
 */
export const useKechengxinxiFindById = (id) => {
    var form = reactive({
        // 预设默认属性，防止渲染错误
        kechengbianhao: '',
        kechengmingcheng: '',
        kechengfenlei: '',
        kechengfengmian: '',
        kechengyaodian: '',
        fabujiaoshi: '',
        kechengxiangqing: '',
        addtime: '',
        issh: '否',
        loading: true, // 添加加载状态
        error: null   // 添加错误状态
    });

    // 防止ID无效导致的错误
    if (!id) {
        form.error = '无效的课程ID';
        form.loading = false;
        console.warn('useKechengxinxiFindById: 无效的ID:', id);
        return form;
    }

    console.log('useKechengxinxiFindById: 开始加载ID为', id, '的课程数据');
    
    // 尝试从缓存获取数据
    const tryLoadFromCache = async () => {
        try {
            // 首先尝试从localStorage获取缓存
            try {
                const cacheKey = `kechengxinxi_${id}`;
                const cachedData = localStorage.getItem(cacheKey);
                
                if (cachedData) {
                    const parsedData = JSON.parse(cachedData);
                    console.log('从localStorage加载数据成功:', parsedData);
                    extend(form, parsedData);
                    form.fromCache = true; // 标记数据来源
                    return true;
                }
            } catch (localStorageError) {
                console.warn('从localStorage加载失败:', localStorageError);
            }
            
            // 再尝试从IndexedDB获取
            const DB = (await import('@/utils/db')).default;
            const localData = await DB.name("kechengxinxi").where("id", id).find();
            if (localData && Object.keys(localData).length > 0) {
                console.log('从DB加载数据成功:', localData);
                extend(form, localData);
                form.fromCache = true; // 标记数据来源
                return true;
            }
            return false;
        } catch (error) {
            console.error('从缓存加载数据失败:', error);
            return false;
        }
    };

    // 创建模拟数据（仅在所有API请求都失败时使用）
    const createMockData = () => {
        const mockData = {
            id: id,
            kechengbianhao: 'MOCK-' + id,
            kechengmingcheng: '临时课程数据',
            kechengfenlei: '1',
            kechengfengmian: '/static/images/default-course.jpg',
            kechengyaodian: '由于网络问题，显示临时数据',
            fabujiaoshi: '系统',
            kechengxiangqing: '<p>正在尝试重新获取数据，请稍后刷新页面...</p>',
            addtime: new Date().toISOString().slice(0, 19).replace('T', ' '),
            issh: '是',
            isMockData: true
        };
        console.log('创建模拟数据:', mockData);
        extend(form, mockData);
    };

    // 执行数据加载
    canKechengxinxiFindById(id)
        .then((res) => {
            console.log('API加载数据成功:', res);
            extend(form, res);
            form.loading = false;
            form.error = null;
            
            // 尝试缓存到localStorage
            try {
                if (res && res.id) {
                    const cacheKey = `kechengxinxi_${res.id}`;
                    localStorage.setItem(cacheKey, JSON.stringify(res));
                    console.log('数据已缓存到localStorage:', cacheKey);
                }
            } catch (cacheError) {
                console.warn('缓存数据失败:', cacheError);
            }
        })
        .catch(async (error) => {
            console.error('API加载数据失败:', error);
            form.error = error.message || '加载课程数据失败';
            
            // 尝试从缓存加载
            const cacheSuccess = await tryLoadFromCache();
            
            if (!cacheSuccess) {
                // 缓存也没有数据，创建模拟数据
                createMockData();
            }
            
            form.loading = false;
        });

    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canKechengxinxiInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengxinxi/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxinxi_insert", res.data);
                        event.emit("kechengxinxi_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

/**
 * 根据数据更新数据库
 * @param data
 * @return {Promise<unknown>}
 */
export const canKechengxinxiUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengxinxi/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxinxi_update", res.data);
                        event.emit("kechengxinxi_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

export const canKechengxinxiCheckIssh = (row) => {
    return new Promise((resolve, reject) => {
        var id = row.id;
        var value = row.issh === "是" ? "否" : "是";
        http.get("/kechengxinxi/admin/checkIssh/", { id, value })
            .json()
            .then(
                (res) => {
                    if (res.code == 0) {
                        row.issh = value;
                    }
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxinxi_update", row);
                        event.emit("kechengxinxi_change", row);
                    }
                },
                (err) => {
                    ElMessageBox.alert(err.message);
                    reject(err);
                }
            );
    });
};

/**
 * 根据id 或者列表id
 * @param id
 * @return {Promise<unknown>}
 */
export const canKechengxinxiDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/kechengxinxi/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxinxi_delete", res.data);
                        event.emit("kechengxinxi_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

export const useKechengxinxishoucang = (id, iss, count) => {
    console.log('调用获取课程收藏状态, ID:', id);
    
    // 确保ID是有效值
    if (!id) {
        console.error('调用获取收藏状态时缺少有效ID');
        return { is_shoucang: ref(false), shoucangCount: ref(0) };
    }
    
    // 确保ID是字符串格式
    const courseId = String(id);
    console.log('处理后的课程ID:', courseId);
    
    // 确保参数是响应式对象
    const is_shoucang = iss ? iss : ref(false);
    const shoucangCount = count ? count : ref(0);
    
    // 获取当前用户信息
    const userStore = useUserStore();
    const username = userStore.session ? userStore.session.username : '';
    
    console.log('初始状态值:', {
        is_shoucang: is_shoucang.value, 
        shoucangCount: shoucangCount.value,
        currentUser: username
    });

    // 构建参数，确保包含用户名和ID是字符串格式
    const params = {
        id: courseId,
        username: username  // 显式传递用户名
    };
    
    console.log('发送收藏状态请求，参数:', params);

    // 检查参数有效性
    if (!params.id || params.id === 'undefined' || params.id === 'null') {
        console.error('无效的课程ID参数:', params.id);
        return { is_shoucang, shoucangCount };
    }

    // 发起请求获取最新状态 - 使用异步处理
    setTimeout(() => {
        http.get("/kechengxinxi/admin/getshoucang/", params)
            .then((res) => {
                console.log('收藏状态响应:', res);
                
                // 处理各种可能的响应格式
                if (res) {
                    // 直接使用响应对象 - 后端返回的是直接数据
                    if (typeof res.is_shoucang !== 'undefined' && typeof res.shoucangCount !== 'undefined') {
                        is_shoucang.value = Boolean(res.is_shoucang);
                        shoucangCount.value = res.shoucangCount;
                        console.log('处理原始响应数据');
                    } 
                    // 响应包含在data属性中
                    else if (res.data && typeof res.data.is_shoucang !== 'undefined' && typeof res.data.shoucangCount !== 'undefined') {
                        is_shoucang.value = Boolean(res.data.is_shoucang);
                        shoucangCount.value = res.data.shoucangCount;
                        console.log('处理data属性中的响应数据');
                    }
                    // 响应可能是code和data的标准格式
                    else if (res.code === 0 && res.data) {
                        // 检查data是否包含必要字段
                        if (typeof res.data.is_shoucang !== 'undefined' && typeof res.data.shoucangCount !== 'undefined') {
                            is_shoucang.value = Boolean(res.data.is_shoucang);
                            shoucangCount.value = res.data.shoucangCount;
                            console.log('处理标准格式响应数据');
                        }
                    }
                    
                    console.log('收藏状态已更新:', {
                        is_shoucang: is_shoucang.value,
                        shoucangCount: shoucangCount.value,
                        user: username
                    });
                } else {
                    console.error('获取收藏状态失败: 响应为空');
                }
            })
            .catch(error => {
                console.error('获取收藏状态请求出错:', error);
            });
    }, 0);

    return { is_shoucang, shoucangCount };
};
