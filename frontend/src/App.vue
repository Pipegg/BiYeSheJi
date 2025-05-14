<script setup>
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useUserStore } from "@/stores";
import { onMounted, ref, watch, onUnmounted } from 'vue';
import Zhu from '@/components/zhinengwenda/zhu.vue'

const userStore = useUserStore();
const tokenRefreshAttempted = ref(false);
const router = useRouter();

// 检查登录结果是否成功
const isSuccessResponse = (res) => {
    // 如果响应有 code=0，视为成功
    if (res && res.code === 0) return true;
    
    // 检查是否有会话数据和token
    if (res && res.session && res.token) return true;
    
    // 如果有嵌套数据，递归检查
    if (res && res.data) return isSuccessResponse(res.data);
    
    return false;
};

// 在组件挂载后进行token登录
onMounted(async () => {
    try {
        // 加入短暂延迟，避免与手动登录冲突
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // 检查是否已经有token和session
        const hasToken = !!userStore.token;
        const hasSession = !!userStore.session && typeof userStore.session === 'object';
        const isLoginValid = userStore.isLogin();
        
        console.log('App挂载时登录状态:', { hasToken, hasSession, isLoginValid });
        
        // 如果已有token但登录状态无效或需要刷新，尝试刷新token
        if (hasToken && (!isLoginValid || !tokenRefreshAttempted.value)) {
            console.log('尝试使用token恢复登录状态');
            tokenRefreshAttempted.value = true;
            
            try {
                const loginResult = await userStore.tokenLogin();
                console.log('Token登录结果:', loginResult);
                
                // 检查是否登录成功
                if (isSuccessResponse(loginResult)) {
                    console.log('Token登录响应有效');
                    
                    // 确保会话状态正确
                    const loginState = userStore.isLogin();
                    if (loginState) {
                        console.log('Token登录成功，会话已恢复');
                    } else {
                        console.warn('Token登录响应正常，但登录状态检查失败');
                        
                        // 尝试从响应中恢复会话数据
                        let sessionData = null;
                        let tokenData = null;
                        
                        // 从各种可能的位置尝试获取会话数据
                        if (loginResult.data && loginResult.data.session) {
                            sessionData = loginResult.data.session;
                            tokenData = loginResult.data.token;
                        } else if (loginResult.session) {
                            sessionData = loginResult.session;
                            tokenData = loginResult.token;
                        }
                        
                        // 如果找到会话数据，尝试修复
                        if (sessionData) {
                            const fixedSession = {...sessionData};
                            // 确保session.id存在
                            if (!fixedSession.id && fixedSession.username) {
                                fixedSession.id = fixedSession.username;
                            }
                            userStore.setSession(fixedSession);
                            
                            // 如果找到token也更新
                            if (tokenData) {
                                userStore.setToken(tokenData);
                            }
                            
                            console.log('已尝试修复会话状态');
                        }
                    }
                } else {
                    console.warn('Token登录失败，清除过期的token');
                    userStore.setToken(null);
                    userStore.setSession(null);
                }
            } catch (error) {
                console.error('Token登录失败:', error);
                // 不要立即清空token，让后续请求继续尝试
            }
        }
    } catch (error) {
        console.error('初始化登录状态失败:', error);
    }
});

// 监听路由变化，在必要时检查或刷新token
watch(() => router.currentRoute.value, async (newRoute) => {
    // 对需要授权的路由，确保token有效
    if (newRoute.meta.authLogin && userStore.token) {
        if (!userStore.isLogin()) {
            console.log('路由需要授权但登录状态无效，尝试刷新token');
            await userStore.tokenLogin();
        }
    }
}, { immediate: true });

// 定期刷新token保持会话活跃
let tokenRefreshInterval;
onMounted(() => {
    // 每15分钟自动刷新一次token确保会话不过期
    tokenRefreshInterval = setInterval(async () => {
        if (userStore.token) {
            console.log('定期刷新token');
            try {
                await userStore.tokenLogin();
            } catch (e) {
                console.error('定期刷新token失败:', e);
            }
        }
    }, 15 * 60 * 1000);
});

// 组件卸载时清理定时器
onUnmounted(() => {
    if (tokenRefreshInterval) {
        clearInterval(tokenRefreshInterval);
    }
});
</script>

<template>
    <RouterView />
    <zhu></zhu>
    <e-chat-dialog></e-chat-dialog>
</template>

<style>
html,
body,
#app {
    height: 100%;
}
</style>
