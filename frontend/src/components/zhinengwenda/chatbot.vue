<template>
    <!--pages/contact/contact.wxml-->
    <div class="chat-list">
        <!-- <div class="gpt-chat-header">
            <img :src="pigImg" alt="GGBond" class="gpt-avatar" />
            <span class="gpt-title">GGBond</span>
        </div> -->
        <div class="chat-body">
            <div class="chat-msg-list">
                <div
                    v-for="(item, idx) in msgList"
                    :key="idx"
                    :class="['chat-row', item.isOneself ? 'chat-row-user' : 'chat-row-bot']"
                >
                    <template v-if="item.isOneself">
                        <div class="chat-bubble chat-bubble-user">
                            <template v-if="isImageMsg(item.content)">
                                <img :src="item.content" class="chat-img" />
                            </template>
                            <template v-else>
                                <span v-html="formatMessage(item.content)"></span>
                            </template>
                        </div>
                        <img :src="getValidUserAvatar(item.touxiang)" class="chat-avatar-user"/>
                    </template>
                    <template v-else>
                        <img :src="item.touxiang || pigImg" class="chat-avatar-bot" />
                        <div class="chat-bubble chat-bubble-bot">
                            <template v-if="isImageMsg(item.content)">
                                <img :src="item.content" class="chat-img" />
                            </template>
                            <template v-else>
                                <span v-html="formatMessage(item.content)"></span>
                            </template>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <div class="gpt-chat-inputbar">
            <el-input
                v-model="inputVal"
                @keyup.enter="sendClick"
                placeholder="请输入问题，按Enter发送"
                class="gpt-input"
                :disabled="loading" 
            />
            <!-- <el-button type="primary" :loading="loading" @click="sendClick" class="gpt-send-btn">发送</el-button> -->
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watchEffect } from "vue";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/user";
import http from "@/utils/ajax/http";
import pigImg from './img.png';
import date from "@/utils/date";
import { marked } from 'marked';
import { formatImageSrc } from '@/utils/utils';
import axios from 'axios';
import config from "@/config";
import { aiHttp } from "@/utils/ajax/http";

const props = defineProps({
    scrollHeight:{
        type:String,
        default:'450px'
    }
});

const userStore = useUserStore();
const inputVal = ref('');
const msgList = ref([]);
const loading = ref(false);
const followUpQuestions = ref([]);
const dialogVisible = ref(false); // 对话框是否可见

// 获取用户ID
const getUserId = () => {
    console.log('getUserId called, current userStore state:', {
        token: userStore.token ? 'exists' : 'null',
        session: userStore.session ? {
            id: userStore.session.id,
            username: userStore.session.username,
            xingming: userStore.session.xingming
        } : 'null',
        isLogin: userStore.isLogin(),
        isUserInfo: userStore.isUserInfo()
    });

    if (!userStore.isLogin()) {
        console.log('用户未登录或登录状态无效');
        ElMessage.warning('请先登录');
        return null;
    }

    // 从 session 中获取用户 ID
    const userId = userStore.session?.id;
    console.log('获取到的用户ID:', userId);
    
    // 如果用户 ID 为空，尝试从 session 的其他字段获取
    if (!userId) {
        const username = userStore.session?.username;
        if (username) {
            console.log('使用用户名作为用户ID:', username);
            return username;
        }
        console.log('用户ID为空');
        ElMessage.warning('用户信息不完整，请重新登录');
        return null;
    }
    return userId;
};

// 获取用户头像
const getUserAvatar = () => {
    if (userStore.isUserInfo() && userStore.session?.touxiang) {
        return userStore.session.touxiang;
    }
    return pigImg;
};

// 获取用户姓名
const getUserName = () => {
    if (!userStore.isUserInfo()) {
        return '未登录';
    }
    return userStore.session?.xingming || '未登录';
};

// 加载历史消息
const loadHistory = async () => {
    const userId = getUserId();
    console.log('当前用户ID:', userId);
    if (!userId) {
        console.log('用户未登录或用户信息不完整，跳过加载历史消息');
        return;
    }

    try {
        // 使用 fetchModel 方式发送请求
        console.log('开始加载历史消息，用户ID:', userId);
        
        // 添加详细的调试信息
        console.log('请求前的认证状态检查:', {
            token: userStore.token ? userStore.token.substring(0, 20) + '...' : 'null',
            loginState: userStore.isLogin(),
            sessionData: JSON.stringify(userStore.session || {}).substring(0, 100)
        });

        // 准备请求配置
        const params = { user_id: userId };
        const requestConfig = {
            headers: {
                'token': userStore.token,
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            // 确保携带cookie
            withCredentials: true
        };
        
        console.log('历史消息请求配置:', {
            url: '/api/chat/history/',
            params,
            headers: requestConfig.headers
        });
        
        // 检查API连接
        let apiSuccessful = false;
        
        // 尝试使用 axios 直接发送请求，绕过 fetchModel
        try {
            console.log('尝试使用 axios 直接发送请求');
            const axiosResponse = await axios.get(config.service_url + '/api/chat/history/', {
                params,
                ...requestConfig
            });
            
            console.log('Axios 历史消息响应:', axiosResponse.data);
            const response = axiosResponse.data;
            
            // 处理响应数据
            if (processHistoryResponse(response)) {
                apiSuccessful = true;
                return; // 成功，不需要继续尝试
            }
        } catch (axiosError) {
            console.error('使用 axios 直接请求失败:', axiosError);
            console.log('尝试使用 aiHttp 专用客户端');
            
            // 第二种尝试：使用 aiHttp 专用客户端
            try {
                // 尝试不同的路径格式
                console.log('尝试标准API路径: /api/chat/history/');
                const aiResponse = await aiHttp.get('/api/chat/history/', {
                    params,
                    headers: requestConfig.headers
                });
                
                console.log('aiHttp 历史消息响应:', aiResponse);
                
                // 检查响应格式
                if (processHistoryResponse(aiResponse)) {
                    apiSuccessful = true;
                    return; // 成功，不需要继续尝试
                }
                
                // 如果标准路径失败，尝试直接的chat路径
                console.log('尝试替代路径: /chatbot/history/');
                const chatResponse = await aiHttp.get('/chatbot/history/', {
                    params,
                    headers: requestConfig.headers
                });
                
                console.log('aiHttp 替代路径响应:', chatResponse);
                
                if (processHistoryResponse(chatResponse)) {
                    apiSuccessful = true;
                    return;
                }
                
                console.warn('aiHttp 响应格式不符合预期，尝试下一种方法。');
            } catch (aiError) {
                console.error('使用 aiHttp 客户端请求失败:', aiError);
            }
            
            console.log('尝试回退到 fetchModel 方式');
        }
        
        // 回退方案：使用原有的 http 工具
        try {
            const response = await http.get('/api/chat/history/', params)
                .then(res => {
                    console.log('fetchModel 历史消息响应:', res);
                    return res;
                });
            
            // 检查响应数据
            if (processHistoryResponse(response)) {
                apiSuccessful = true;
                return;
            }
        } catch (httpError) {
            console.error('使用 http 工具请求失败:', httpError);
        }
        
        // 如果所有请求都失败，使用模拟数据
        if (!apiSuccessful) {
            console.warn('所有API请求失败，使用模拟数据');
            createMockChatHistory();
        }
    } catch (error) {
        console.error('加载历史消息失败:', error);
        console.error('错误详情:', {
            message: error.message,
            name: error.name,
            stack: error.stack,
            response: error.response ? {
                data: error.response.data,
                status: error.response.status,
                statusText: error.response.statusText,
                headers: error.response.headers
            } : 'No response',
            config: error.config ? {
                url: error.config.url,
                method: error.config.method,
                params: error.config.params,
                data: error.config.data,
                headers: error.config.headers,
                timeout: error.config.timeout,
                withCredentials: error.config.withCredentials
            } : 'No config'
        });
        
        // 根据错误类型显示不同的错误消息
        if (error.response?.status === 400) {
            ElMessage.error('请求参数错误：' + (error.response.data?.error || error.response.data?.msg || '未知错误'));
        } else if (error.response?.status === 401) {
            ElMessage.error('未授权：请重新登录');
            // 添加自动重新登录的逻辑
            try {
                console.log('尝试重新登录...');
                const loginResult = await userStore.tokenLogin();
                if (loginResult && loginResult.code === 0) {
                    console.log('重新登录成功，重试加载历史消息');
                    setTimeout(() => loadHistory(), 500);
                    return;
                }
            } catch (loginError) {
                console.error('重新登录失败:', loginError);
            }
        } else if (error.response?.status === 500) {
            ElMessage.error('服务器错误：' + (error.response.data?.error || error.response.data?.msg || '未知错误'));
        } else {
            ElMessage.error('加载历史消息失败：' + (error.response?.data?.error || error.response?.data?.msg || error.message || '未知错误'));
        }
        
        // 打印请求和响应详情
        console.log('完整的请求信息:', {
            url: error.config?.url,
            method: error.config?.method,
            headers: error.config?.headers,
            params: error.config?.params,
            data: error.config?.data
        });
        console.log('完整的响应信息:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            headers: error.response?.headers,
            data: error.response?.data
        });
        
        // 如果所有请求失败，使用模拟数据
        createMockChatHistory();
    }
};

// 处理历史消息响应的通用函数
const processHistoryResponse = (response) => {
    // 直接是数组
    if (Array.isArray(response)) {
        msgList.value = response.map(msg => ({
            content: msg.content,
            isOneself: msg.role === 'user',
            addtime: msg.timestamp,
            touxiang: msg.role === 'user' ? formatImageSrc(userStore.session?.touxiang) : pigImg,
            nickname: msg.role === 'user' ? getUserName() : 'AI助手'
        }));
        console.log('成功加载历史消息，消息数量:', msgList.value.length);
        return true;
    } 
    // response.data 是数组
    else if (response && response.data && Array.isArray(response.data)) {
        console.log('从 response.data 中提取历史消息');
        msgList.value = response.data.map(msg => ({
            content: msg.content,
            isOneself: msg.role === 'user',
            addtime: msg.timestamp,
            touxiang: msg.role === 'user' ? formatImageSrc(userStore.session?.touxiang) : pigImg,
            nickname: msg.role === 'user' ? getUserName() : 'AI助手'
        }));
        console.log('成功加载历史消息，消息数量:', msgList.value.length);
        return true;
    } 
    // 标准响应格式 {code: 0, data: [...]}
    else if (response && response.code === 0 && response.data && Array.isArray(response.data)) {
        console.log('从标准响应格式中提取历史消息');
        msgList.value = response.data.map(msg => ({
            content: msg.content,
            isOneself: msg.role === 'user',
            addtime: msg.timestamp,
            touxiang: msg.role === 'user' ? formatImageSrc(userStore.session?.touxiang) : pigImg,
            nickname: msg.role === 'user' ? getUserName() : 'AI助手'
        }));
        console.log('成功加载历史消息，消息数量:', msgList.value.length);
        return true;
    } 
    // 非标准格式 {messages: [...]} 
    else if (response && response.messages && Array.isArray(response.messages)) {
        console.log('从 response.messages 中提取历史消息');
        msgList.value = response.messages.map(msg => ({
            content: msg.content,
            isOneself: msg.role === 'user',
            addtime: msg.timestamp || msg.addtime || date('Y-m-d H:i:s'),
            touxiang: msg.role === 'user' ? formatImageSrc(userStore.session?.touxiang) : pigImg,
            nickname: msg.role === 'user' ? getUserName() : 'AI助手'
        }));
        console.log('成功加载历史消息，消息数量:', msgList.value.length);
        return true;
    }
    
    console.error('历史消息响应格式错误:', response);
    console.log('响应类型:', typeof response);
    console.log('响应结构:', JSON.stringify(response).substring(0, 200));
    return false;
};

// 创建模拟数据作为后备方案
const createMockChatHistory = () => {
    console.log('创建模拟聊天历史');
    msgList.value = [
        {
            content: "您好，我是AI助手，有什么可以帮助您的吗？",
            isOneself: false,
            addtime: date('Y-m-d H:i:s', Date.now() - 3600000),
            touxiang: pigImg,
            nickname: 'AI助手'
        }
    ];
    console.log('已创建模拟聊天历史');
};

const sendClick = () => {
    const content = inputVal.value;
    if (!content) {
        ElMessage.error('请填写内容');
        return;
    }
    sendContent(content);
};

const sendContent = async (content) => {
    if (!content.trim()) {
        ElMessage.warning('请输入内容');
        return;
    }

    // 检查登录状态
    const userId = getUserId();
    console.log('发送消息时检查用户ID:', userId);
    if (!userId) {
        console.log('用户未登录，无法发送消息');
        ElMessage.error('请先登录');
        return;
    }

    loading.value = true;
    followUpQuestions.value = [];

    // 添加用户消息
    const userMessage = {
        content: content,
        isOneself: true,
        addtime: date('Y-m-d H:i:s'),
        touxiang: formatImageSrc(userStore.session?.touxiang),
        nickname: getUserName()
    };
    msgList.value.push(userMessage);
    inputVal.value = '';

    try {
        console.log('发送请求:', {
            question: content,
            user_id: userId
        });

        // 添加详细的调试信息
        console.log('请求前的认证状态检查:', {
            token: userStore.token ? userStore.token.substring(0, 20) + '...' : 'null',
            loginState: userStore.isLogin(),
            sessionData: JSON.stringify(userStore.session || {}).substring(0, 100)
        });

        // 准备请求配置
        const params = { 
            question: content,
            user_id: userId
        };
        const requestConfig = {
            headers: {
                'token': userStore.token,
                'Authorization': `Bearer ${userStore.token}`,
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            withCredentials: true
        };

        let messageSuccess = false;
        
        // 第一种尝试：使用标准http工具
        try {
            console.log('尝试使用标准HTTP发送消息');
            const response = await http.post('/chatbot/wenti/', params, requestConfig);
            console.log('消息响应:', response);
            
            if (response && response.data && response.data.answer) {
                // 添加AI回复
                const aiMessage = {
                    content: response.data.answer,
                    isOneself: false,
                    addtime: date('Y-m-d H:i:s'),
                    touxiang: pigImg,
                    nickname: 'AI助手'
                };
                msgList.value.push(aiMessage);
                messageSuccess = true;
                
                // 尝试获取后续问题建议
                try {
                    const followUpResponse = await http.post('/api/chat/follow-up/', {
                        question: content,
                        answer: response.data.answer
                    });
                    if (followUpResponse && followUpResponse.questions) {
                        followUpQuestions.value = followUpResponse.questions;
                    }
                } catch (followUpError) {
                    console.error('获取后续问题失败:', followUpError);
                }
            }
        } catch (httpError) {
            console.error('使用HTTP发送消息失败:', httpError);
            
            // 第二种尝试：使用aiHttp专用客户端
            try {
                console.log('尝试使用aiHttp发送消息');
                const aiResponse = await aiHttp.post('/chatbot/wenti/', params);
                console.log('aiHttp消息响应:', aiResponse);
                
                if (aiResponse && aiResponse.data && aiResponse.data.answer) {
                    // 添加AI回复
                    const aiMessage = {
                        content: aiResponse.data.answer,
                        isOneself: false,
                        addtime: date('Y-m-d H:i:s'),
                        touxiang: pigImg,
                        nickname: 'AI助手'
                    };
                    msgList.value.push(aiMessage);
                    messageSuccess = true;
                } else if (aiResponse && aiResponse.answer) {
                    // 响应格式可能直接包含answer
                    const aiMessage = {
                        content: aiResponse.answer,
                        isOneself: false,
                        addtime: date('Y-m-d H:i:s'),
                        touxiang: pigImg,
                        nickname: 'AI助手'
                    };
                    msgList.value.push(aiMessage);
                    messageSuccess = true;
                } else {
                    console.error('AI响应格式错误:', aiResponse);
                }
            } catch (aiError) {
                console.error('使用aiHttp发送消息失败:', aiError);
                
                // 第三种尝试：使用axios直接发送
                try {
                    console.log('尝试使用axios直接发送消息');
                    const axiosResponse = await axios.post(config.service_url + '/chatbot/wenti/', params, requestConfig);
                    console.log('axios消息响应:', axiosResponse.data);
                    
                    const axiosData = axiosResponse.data;
                    if (axiosData && axiosData.data && axiosData.data.answer) {
                        // 添加AI回复
                        const aiMessage = {
                            content: axiosData.data.answer,
                            isOneself: false,
                            addtime: date('Y-m-d H:i:s'),
                            touxiang: pigImg,
                            nickname: 'AI助手'
                        };
                        msgList.value.push(aiMessage);
                        messageSuccess = true;
                    } else if (axiosData && axiosData.answer) {
                        // 响应格式可能直接包含answer
                        const aiMessage = {
                            content: axiosData.answer,
                            isOneself: false,
                            addtime: date('Y-m-d H:i:s'),
                            touxiang: pigImg,
                            nickname: 'AI助手'
                        };
                        msgList.value.push(aiMessage);
                        messageSuccess = true;
                    } else {
                        console.error('axios响应格式错误:', axiosData);
                    }
                } catch (axiosError) {
                    console.error('使用axios发送消息失败:', axiosError);
                }
            }
        }
        
        // 如果所有方法都失败，添加错误消息
        if (!messageSuccess) {
            console.error('所有发送消息方法都失败，添加错误提示');
            const errorMessage = {
                content: '抱歉，我暂时无法回答这个问题。请稍后再试。',
                isOneself: false,
                addtime: date('Y-m-d H:i:s'),
                touxiang: pigImg,
                nickname: 'AI助手'
            };
            msgList.value.push(errorMessage);
        }
    } catch (error) {
        console.error('发送消息失败:', error);
        console.error('错误详情:', {
            message: error.message,
            name: error.name,
            stack: error.stack,
            response: error.response ? {
                data: error.response.data,
                status: error.response.status,
                statusText: error.response.statusText,
                headers: error.response.headers
            } : 'No response',
            config: error.config ? {
                url: error.config.url,
                method: error.config.method,
                params: error.config.params,
                data: error.config.data,
                headers: error.config.headers,
                timeout: error.config.timeout,
                withCredentials: error.config.withCredentials
            } : 'No config'
        });
        
        // 根据错误类型显示不同的错误消息
        if (error.response?.status === 400) {
            ElMessage.error('请求参数错误：' + (error.response.data?.error || error.response.data?.msg || '未知错误'));
        } else if (error.response?.status === 401) {
            ElMessage.error('未授权：请重新登录');
        } else if (error.response?.status === 500) {
            ElMessage.error('服务器错误：' + (error.response.data?.error || error.response.data?.msg || '未知错误'));
        } else {
            ElMessage.error('发送消息失败：' + (error.response?.data?.error || error.response?.data?.msg || error.message || '未知错误'));
        }
        
        // 添加错误提示消息
        const errorMessage = {
            content: '抱歉，我暂时无法回答这个问题。请稍后再试。',
            isOneself: false,
            addtime: date('Y-m-d H:i:s'),
            touxiang: pigImg,
            nickname: 'AI助手'
        };
        msgList.value.push(errorMessage);
    } finally {
        loading.value = false;
    }
};

// 选择后续问题
const selectFollowUpQuestion = (q) => {
    inputVal.value = q;
    sendClick();
};

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
    return marked.parse(content);
};

const getValidUserAvatar = (url) => {
    if (url && typeof url === 'string' && !url.includes('broken') && !url.endsWith('.svg')) {
        // 如果是以 /static/ 开头的相对路径，补全为绝对路径
        if (url.startsWith('/static/')) {
            return window.location.origin + url;
        }
        return url;
    }
    return pigImg;
};

const onMaskClick = (e) => {
    if (e.target === e.currentTarget) {
        dialogVisible.value = false;
    }
};

// 检查消息是否为图片
const isImageMsg = (content) => {
    return typeof content === 'string' && /\.(jpeg|jpg|gif|png|webp)$/i.test(content);
};

onMounted(() => {
    console.log('Chatbot component mounted');
    console.log('Current userStore state:', {
        token: userStore.token ? 'exists' : 'null',
        session: userStore.session ? {
            id: userStore.session.id,
            username: userStore.session.username
        } : 'null'
    });
    
    const userId = getUserId();
    console.log('组件挂载，当前用户ID:', userId);
    // 确保用户已登录
    if (userId) {
        loadHistory();
    } else {
        console.log('用户未登录，等待登录状态更新');
    }
});

watchEffect(() => {
  console.log('msgList:', msgList.value);
});
</script>

<style scoped lang="scss">
.chat-list {
    background: rgba(245, 245, 247, 0.0);
    min-height: 100%;
    display: flex;
    flex-direction: column; // 垂直布局
    height: 500px;
    width: 700px;
    border-radius: 16px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.00);
}
.gpt-chat-header {
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 28px;
    border-bottom: 1px solid rgba(245, 245, 247, 0.0);
    border-radius: 16px 16px 0 0;
    background: rgba(245, 245, 247, 0.0);
    .gpt-avatar {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        margin-right: 12px;
    }
    .gpt-title {
        font-size: 20px;
        font-weight: 600;
        color: #222;
        letter-spacing: 1px;
    }
}
.chat-body {
    flex: 1;
    overflow-y: auto;
    padding: 0;
    background: rgba(245, 245, 247, 0.0);
}
.chat-msg-list {
    padding: 24px 0;
    min-height: 100%;
}
.chat-row {
    width: 100%;
    display: flex;
    flex-flow: column;
    align-items: flex-start;
    margin-bottom: 18px;
    padding: 0;
}
.chat-row-bot {
    flex-direction: row;
    justify-content: flex-start;
}
.chat-row-user {
    flex-direction: row;
    justify-content: flex-end;
}
.chat-avatar-user {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    margin: 0px 10px 10px 10px;
    float: right;
    background: rgba(245, 245, 247, 0.0);
    border: 1px solid rgba(245, 245, 247, 0.0);
    object-fit: cover;
    display: flex;
    justify-content: flex-end;
}
.chat-avatar-bot {
    width: 40px;
    height: 40px;
    border-radius: 6px;
    margin: 0px 10px 10px 10px;
    background: rgba(245, 245, 247, 0.0);
    border: 1px solid rgba(245, 245, 247, 0.0);
    object-fit: cover;
    display: flex;
    align-items: flex-start;
}
.chat-bubble {
    max-width: 70%;
    padding: 0px 10px 0px 10px; /* 上下左右内边距 */
    font-size: 15px;
    line-height: 1.7;
    display: flex;
    align-items: center;
    min-height: 36px;
    word-break: break-word;
    box-shadow: 0 1px 4px rgba(0,0,0,0);
    // z-index: 10;
}
.chat-bubble-bot {
    background: #fff;
    color: #222;
    border-radius: 0 8px 8px 8px;
    margin-left: 0px;
    margin-right: 0;
}
.chat-bubble-user {
    background: #fff;
    color: #222;
    border-radius: 8px 0 8px 8px;
    margin-right: 0px;
    margin-left: 0;
}
.chat-img {
    max-width: 120px;
    max-height: 120px;
    border-radius: 8px;
    display: block;
    margin: 0 auto;
}
.gpt-chat-inputbar {
    display: flex;
    align-items: center;
    padding: 16px 20px 16px 20px;
    background: rgba(245, 245, 247, 0.0);
    border-top: 1px solid rgba(245, 245, 247, 0.0);
    border-radius: 0 0 16px 16px;
    box-shadow: 0 -2px 8px rgba(0,0,0,0.03);
    gap: 12px;
}
.gpt-input {
    flex: 1;
    border-radius: 8px;
    font-size: 15px;
    min-height: 40px;
}
.gpt-send-btn {
    min-width: 72px;
    border-radius: 8px;
    font-size: 15px;
}
.gpt-mask {
    position: fixed;
    z-index: 2000;
    left: 0; top: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
}
.gpt-center {
    display: flex;
    justify-content: center;
    align-items: center;
}
/* 针对 Webkit 内核浏览器（Chrome、Edge、Safari） */
.chat-body::-webkit-scrollbar,
.chat-msg-list::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
  background: rgba(0,0,0,0.00); /* 滚动条轨道背景 */
}

.chat-body::-webkit-scrollbar-thumb,
.chat-msg-list::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.0); /* 滚动条滑块颜色 */
  border-radius: 8px;
}

.chat-body::-webkit-scrollbar-thumb:hover,
.chat-msg-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0,0,0,0.0); /* 滑块悬停颜色 */
}
</style>