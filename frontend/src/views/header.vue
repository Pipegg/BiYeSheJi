<template>
    <div class="main-header" :class="{'main-header-fixed':isFixMenuDesktop, hover:isHover}" style="">
        <div class="header-top">
            <div class="auto-1400 clearfix">
                <div class="top-left fl">{{ config.title }}</div>
                <div class="top-right fr">
                    <ul>
                        <li>全国免费咨询热线：xxxxxxx</li>
                        <li class="sli">
                            <form action="javascript:;" @submit="searchKeyword" class="search-form">
                                <input type="search" class="search-input" :value="keyword" @input="keyword = $event.target.value" placeholder="请输入关键字" />
                                <button type="submit" class="search-btn">
                                    <i class="fa fa-search"></i>
                                </button>
                            </form>
                        </li>
                        <template v-if="$session.username">
                            <li class="sli">
                                <a href="javascript:;">
                                    <e-chat-button></e-chat-button>
                                </a>
                            </li>
                            <li class="sli">
                                <span class="aicf" v-if="$session.touxiang"><img :src="$formatImageSrc($session.touxiang)" /></span>
                                <a href="javascript:;">{{ $session.username }}</a>
                            </li>
                            <li class="sli user-icon-but">
                                <router-link to="/admin/sy">个人中心</router-link>
                                <span>/</span>
                                <a href="javascript:;" @click="logout">退出登录</a>
                            </li>
                        </template>
                        <template v-else>
                            <li class="sli user-icon-but">
                                <a href="javascript:;" @click="showLogin">登录</a>
                            </li>
                        </template>
                    </ul>
                    <div class="login-model" v-if="!$session.username" @click.stop.prevent :class="{'show-model':isShowLogin}" :style="{height: loginModelHeight}">
                        <div class="login-box" ref="loginBoxRef">
                            <form action="javascript:;">
                                <div class="login-input input-username">
                                    <span class="input-title">用户名：</span>
                                    <input type="text" class="input" v-model="loginForm.username" name="username" placeholder="输入用户名" />
                                    <span class="line"></span>
                                </div>
                                <div class="login-input input-password">
                                    <span class="input-title">密码：</span>
                                    <input type="password" class="input" v-model="loginForm.pwd" name="pwd" placeholder="输入密码" />
                                    <span class="line"></span>
                                </div>
                                <div class="login-input input-captch">
                                    <span class="input-title">验证码：</span>
                                    <input type="text" class="input" name="pagerandom" v-model="loginForm.pagerandom" placeholder="输入验证码" />
                                    <span class="line"></span>
                                    
                                    <!-- 如果验证码URL存在，显示图片 -->
                                    <img v-if="captchaUrl" 
                                         :src="captchaUrl" 
                                         @click="loadCaptcha" 
                                         @error="handleImgError" 
                                         class="captch" 
                                         alt="点击刷新验证码" 
                                         title="点击刷新验证码" />
                                    
                                    <!-- 如果验证码URL不存在，显示加载提示或重试按钮 -->
                                    <div v-else 
                                         @click="loadCaptcha" 
                                         class="captch" 
                                         style="text-align:center;line-height:30px;font-size:12px;cursor:pointer;background:#f2f2f2;color:#555;">
                                        {{ isLoadingCaptcha ? '加载中...' : '点击获取验证码' }}
                                    </div>
                                </div>
                                <div class="login-input input-cx" v-if="rules.length > 1">
                                    <select class="input" name="cx" v-model="loginForm.cx" @change="loginForm.cx = $event.target.value">
                                        <option :value="o" v-for="o in rules" :key="o">{{ o }}</option>
                                    </select>
                                    <span class="line"></span>
                                </div>
                                <div class="login-btn">
                                    <button class="input-btn-bottom" type="button" @click="onLogin">登录</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="" ref="desktop">
            <div class="main-box ms300">
                <div class="auto-1400">
                    <div class="logo-box fl">
                        <div class="logo">
                            <a href="javascript:;" title="">
                                {{ config.title }}
                                <!--<img height="65" src="@assets/images/logo.png">-->
                            </a>
                        </div>
                    </div>
                    <div class="fl adTxt"></div>
                    <nav class="main-menu ms300 fl">
                        <div class="mobile mobile-close" @click="isHover=false">
                            <i class="fa fa-close"></i>
                        </div>
                        <ul class="navigation">
                            <li :class="{'active-menu':isFullPathActive('/index')}">
                                <router-link :to="'/index'" title="首页"> 首页 </router-link>
                            </li>
                            <li :class="{'active-menu':isFullPathActive({path:'/kechengxinxi'})}">
                                <router-link :to="{path:'/kechengxinxi'}" title="课程信息"> 课程信息 </router-link>
                                <div class="sub-menu">
                                    <div class="items">
                                        <div class="item" v-for="(m,k) in listMenukechengfenlei" :key="m.id">
                                            <router-link class="ms300" :to="{path:'/kechengxinxi',query: { kechengfenlei:m.id } }" :title="m.fenleimingcheng">
                                                {{ m.fenleimingcheng }}
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li :class="{'active-menu':isFullPathActive({path:'/learning-path'})}">
                                <router-link v-if="userState.isLogin()" :to="{path:'/learning-path'}" title="学习路径"> 学习路径 </router-link>
                                <a v-else href="javascript:void(0)" @click="handleLearningPathClick" title="学习路径"> 学习路径 </a>
                            </li>
                            <li :class="{'active-menu':isFullPathActive({path:'/luntanjiaoliu'})}">
                                <router-link :to="{path:'/luntanjiaoliu'}" title="论坛交流"> 论坛交流 </router-link>
                                <div class="sub-menu">
                                    <div class="items">
                                        <div class="item" v-for="(m,k) in listMenuluntanfenlei" :key="m.id">
                                            <router-link class="ms300" :to="{path:'/luntanjiaoliu',query: { fenlei:m.id } }" :title="m.fenleimingcheng">
                                                {{ m.fenleimingcheng }}
                                            </router-link>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <li :class="{'active-menu':isFullPathActive({path:'/xuesheng/add'})}">
                                <router-link :to="{path:'/xuesheng/add'}" title="学生注册"> 学生注册 </router-link>
                            </li>
                            <li :class="{'active-menu':isFullPathActive('/login')}">
                                <router-link :to="'/login'" title="后台登录"> 后台登录 </router-link>
                            </li>
                        </ul>
                    </nav>
                    <div class="nav-toggler">
                        <button class="hidden-bar-opener">
                            <span class="aicf"><img src="@/assets/images/nav-cd.png" /></span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="mobile mobile-mask" @click="isHover=false"></div>
    </div>
</template>
<script setup>
    import { useRouter, useRoute } from "vue-router";
    import { computed, ref, reactive, watch, onMounted, onBeforeUnmount } from "vue";
    import { logout, session, useEvent } from "@/utils";
    import config from "@/config";
    import DB from "@/utils/db";
    import { Search } from "@element-plus/icons-vue";
    import { isObject } from "@/utils/extend";
    import { isFullPathActive, isPathActive } from "@/router/router-utils";
    import { useUserStore } from "@/stores";
    import domEvent from "@/utils/dom-event";
    import { captch } from "@/utils/utils";
    import { canLogin } from "@/stores";
    import { ElMessage, ElMessageBox } from "element-plus";

    const isShowLogin = ref(false);
    const loginBoxRef = ref(null);
    const captchaUrl = ref("");
    const isLoadingCaptcha = ref(false);
    const rules = ["学生", "教师"];
    const loginForm = reactive({
        username: "",
        pwd: "",
        cx: rules[0],
        /* 验证码段 */
        pagerandom: "",
        a: "a",
        /* 验证码段 */
    });
    
    const loadCaptcha = () => {
        isLoadingCaptcha.value = true;
        captchaUrl.value = '';
        
        captch().then((res) => {
            isLoadingCaptcha.value = false;
            
            // 存储token
            loginForm.captchToken = res.token;
            
            // 确保URL有效后再设置到图片元素
            if (res.url && res.url.startsWith('data:image')) {
                captchaUrl.value = res.url;
            } else {
                ElMessage.error('验证码格式不正确，请重试');
            }
        }).catch(error => {
            isLoadingCaptcha.value = false;
            ElMessage.error('验证码加载失败，点击重试');
            // 2秒后自动重试
            setTimeout(() => {
                loadCaptcha();
            }, 2000);
        });
    };

    const onLogin = async () => {
        try {
            // 发送登录开始事件
            window.dispatchEvent(new CustomEvent('manual-login-start'));
            
            // 获取用户状态管理
            const userStore = useUserStore();
            
            // 登录请求
            const res = await canLogin(loginForm);
            console.log('登录响应:', res);
            
            // 检查登录状态
            if (res.code === 0) {
                // 等待状态同步
                await new Promise(resolve => setTimeout(resolve, 100));
                
                // 登录状态检查
                const loginState = userStore.isLogin();
                console.log('登录状态检查:', loginState);
                
                if (loginState) {
                    // 登录成功
                    ElMessage.success({
                        message: `登录成功，欢迎 ${userStore.session.username || '用户'}`,
                        duration: 2000
                    });
                    
                    // 关闭登录框
                    isShowLogin.value = false;
                    
                    // 延迟处理页面跳转
                    setTimeout(() => {
                        if (window.location.pathname === '/login') {
                            window.location.href = '/';
                        } else {
                            // 使用路由刷新替代全页面刷新，避免状态丢失
                            const currentRoute = router.currentRoute.value;
                            router.replace({
                                path: '/refresh',
                                query: { redirect: currentRoute.fullPath }
                            }).then(() => {
                                router.replace(currentRoute.fullPath);
                            });
                        }
                    }, 1000);
                } else {
                    // 登录成功但状态异常
                    console.error('登录状态不一致:', userStore);
                    ElMessage.warning({
                        message: "登录状态异常，正在尝试修复...",
                        duration: 3000
                    });
                    
                    // 尝试修复session
                    try {
                        if (res.session) {
                            const fixedSession = {...res.session};
                            if (!fixedSession.id && fixedSession.username) {
                                fixedSession.id = fixedSession.username;
                            }
                            userStore.setSession(fixedSession);
                            userStore.setToken(res.token);
                        } else if (res.data && res.data.session) {
                            const fixedSession = {...res.data.session};
                            if (!fixedSession.id && fixedSession.username) {
                                fixedSession.id = fixedSession.username;
                            }
                            userStore.setSession(fixedSession);
                            userStore.setToken(res.data.token);
                        }
                        
                        // 再次检查登录状态
                        const fixedLoginState = userStore.isLogin();
                        if (fixedLoginState) {
                            ElMessage.success({
                                message: `登录状态已修复，欢迎 ${userStore.session.username || '用户'}`,
                                duration: 2000
                            });
                            
                            // 关闭登录框
                            isShowLogin.value = false;
                            
                            // 延迟处理页面跳转
                            setTimeout(() => {
                                if (window.location.pathname === '/login') {
                                    window.location.href = '/';
                                } else {
                                    // 使用路由刷新替代全页面刷新，避免状态丢失
                                    const currentRoute = router.currentRoute.value;
                                    router.replace({
                                        path: '/refresh',
                                        query: { redirect: currentRoute.fullPath }
                                    }).then(() => {
                                        router.replace(currentRoute.fullPath);
                                    });
                                }
                            }, 1000);
                        } else {
                            ElMessage.error({
                                message: "登录状态修复失败，请重新登录",
                                duration: 3000
                            });
                            loadCaptcha();
                        }
                    } catch (e) {
                        console.error('修复登录状态出错:', e);
                        ElMessage.error({
                            message: "登录状态修复出错，请重新登录",
                            duration: 3000
                        });
                        loadCaptcha();
                    }
                }
            } else {
                // 登录失败
                if (res.code === 20) {
                    // 验证码错误，重新加载验证码
                    loadCaptcha();
                }
                
                ElMessage.error({
                    message: res.msg || '登录失败，请检查用户名和密码',
                    duration: 3000
                });
            }
        } catch (error) {
            console.error('登录过程出错:', error);
            ElMessage.error({
                message: '登录请求失败，请稍后重试',
                duration: 3000
            });
        } finally {
            // 发送登录结束事件
            window.dispatchEvent(new CustomEvent('manual-login-end'));
        }
    };
    const loginModelHeight = computed(() => {
        if (isShowLogin.value) {
            return loginBoxRef.value.getBoundingClientRect().height + "px";
        } else {
            return 0;
        }
    });
    const showLogin = (e) => {
        e.stopPropagation();
        e.preventDefault();
        if (!isShowLogin.value) {
            loginForm.username = "";
            loginForm.pwd = "";
            loginForm.pagerandom = "";
            loginForm.cx = rules[0];
            loadCaptcha();
            domEvent.once(document, "click", () => {
                isShowLogin.value = false;
            });
        }
        isShowLogin.value = !isShowLogin.value;
    };

    const router = useRouter();
    const userState = useUserStore();

    const isHover = ref(false);

    const keyword = ref("");
    const searchKeyword = () => {
        var filter = {};
        filter["kechengmingcheng"] = keyword.value;
        router.push({
            path: "/kechengxinxi",
            query: filter,
        });
    };

    const loadListMenu = async (module, target) => {
        try {
            const result = await DB.name(module)
                .order("id desc")
                .select()
                .catch(err => {
                    console.error(`加载${module}菜单失败:`, err);
                    return [];
                });
                
            target.value = result || [];
        } catch (err) {
            console.error(`加载${module}菜单出错:`, err);
            target.value = [];
        }
    };

    const route = useRoute();
    const listMenukechengfenlei = ref([]);
    loadListMenu("kechengfenlei", listMenukechengfenlei);
    const listMenuluntanfenlei = ref([]);
    loadListMenu("luntanfenlei", listMenuluntanfenlei);

    const isFixMenuDesktop = ref(false);
    const desktop = ref(null);

    const onScroll = () => {
        if (desktop.value) {
            let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            var rect = desktop.value.getBoundingClientRect();
            var top = rect.top + scrollTop;
            if (scrollTop > top) {
                isFixMenuDesktop.value = true;
            } else {
                isFixMenuDesktop.value = false;
            }
        }
    };

    const onLoginFormEvent = () => {
        showLogin({ stopPropagation: () => {}, preventDefault: () => {} });
    };
    
    // 在 onMounted 添加事件监听器
    onMounted(() => {
        onScroll();
        domEvent.on(window, "scroll", onScroll);
        
        // 添加全局登录事件监听器
        window.addEventListener('show-login-form', onLoginFormEvent);
    });
    
    onBeforeUnmount(() => {
        domEvent.off(window, "scroll", onScroll);
        
        // 移除全局登录事件监听器
        window.removeEventListener('show-login-form', onLoginFormEvent);
    });

    const status = ref(false);
    watch(
        () => route,
        () => {
            status.value = false;
        },
        { deep: true }
    );

    const handleImgError = (e) => {
        // 清空当前验证码URL
        captchaUrl.value = '';
        ElMessage.error('验证码图片显示失败，正在重新获取');
        
        // 延迟重试，避免频繁请求
        setTimeout(() => {
            loadCaptcha();
        }, 1500);
    };

    const handleLearningPathClick = (e) => {
        e.preventDefault();
        ElMessageBox.confirm("您需要先登录才能访问学习路径，是否立即登录？", "提示", {
            confirmButtonText: "立即登录",
            cancelButtonText: "取消",
            type: "warning"
        }).then(() => {
            // 显示登录框
            showLogin({ stopPropagation: () => {}, preventDefault: () => {} });
        }).catch(() => {
            // 用户取消登录操作，不做任何事
        });
    };
</script>

<style lang="scss" type="text/scss" scoped>
    .main-header {
        width: 100%;
        height: 128px;
        background: #ffffff;
        --main-header-bgckground: var(--theme-primary-color, #5abdcb);

        .mobile {
            display: none;
        }
        .auto-1400 {
            width: 1400px;
            padding: 0 10px;
            display: table;
            margin: 0 auto;
        }

        .login-model {
            position: absolute;
            right: 0;
            top: 40px;
            width: 300px;
            z-index: 100;
            background: var(--main-header-bgckground);
            height: 0;
            overflow: hidden;
            transition: all 0.3s ease-in-out;
            input,
            select,
            input:focus,
            input:active,
            select:focus,
            select:active {
                outline: none;
            }
            .login-box {
                padding: 15px;
                .login-input {
                    margin-bottom: 10px;
                    position: relative;
                    .captch {
                        position: absolute;
                        right: 0;
                        top: 0;
                        width: 100px;
                        height: 30px;
                    }
                }
                .input {
                    font-size: 14px;
                    width: 100%;
                    border: none;
                    border-radius: 0;
                    padding: 8px 10px;
                    color: #FFFFFF;
                    background: transparent;
                    border-bottom: 1px solid #a6a6a6;
                    position: relative;
                }
                select.input option {
                    color: var(--main-header-bgckground);
                }
                .input + .line {
                    position: absolute;
                    left: 0;
                    bottom: 0;
                    height: 1px;
                    width: 0;
                    transition: width 0.3s ease-in-out;
                    background: #ffffff;
                }
                .input-title {
                    position: absolute;
                    display: none;
                    left: 0;
                    top: 0;
                    padding: 8px 0;
                    width: 60px;
                    text-align: right;
                }
                .input:focus + .line {
                    width: 100%;
                }
                .input::placeholder {
                    color: #FFFFFF;
                }
                .input-btn-bottom {
                    width: 100%;
                    border-radius: 24px;
                    padding: 10px 0;
                    background: #FFFFFF;
                    font-size: 18px;
                    border: none;
                    color: var(--main-header-bgckground);
                }
            }
        }
        .login-model.show-model {
            border-radius: 0 0 5px 5px;
        }

        .fl {
            float: left;
        }

        .fr {
            float: right;
        }

        .header-top {
            background: var(--main-header-bgckground);
            color: #ffffff;
            font-size: 13px;
            height: 40px;
            /*display: flex;
            align-items: center;
            justify-content: space-between;*/

            .top-left {
                line-height: 40px;
                font-size: 14px;
            }

            .top-right {
                position: relative;
                ul {
                    display: flex;
                    align-items: center;
                    height: 40px;

                    li {
                        position: relative;
                        line-height: 24px;
                        margin-right: 10px;
                        display: flex;
                        align-items: center;

                        .aicf {
                            border-radius: 50%;
                            overflow: hidden;
                            font-size: 14px;
                            margin-right: 6px;
                            width: 16px;
                            height: 16px;
                        }

                        a {
                            position: relative;
                            color: #ffffff;
                        }
                    }

                    li.sli {
                        padding: 0 10px;
                        border-radius: 24px;
                        background: #fff;
                        color: var(--main-header-bgckground);
                        transition: all 300ms;

                        a {
                            color: var(--main-header-bgckground);
                        }
                    }

                    li.cart {
                        margin-right: 15px;
                        display: flex;
                        align-items: center;
                        cursor: pointer;
                        .ico {
                            color: #f5b69a;
                            margin-right: 5px;
                        }
                        .cart-num {
                            margin-left: 5px;
                        }
                    }
                    li.cart:hover {
                        color: #f5b69a;
                    }

                    .user-icon-but {
                        span {
                            margin-left: 8px;
                            margin-right: 8px;
                            color: #dddddd;
                        }
                    }

                    .search-form {
                        display: flex;
                        align-items: center;

                        .search-input {
                            color: #0b0b0b;
                        }

                        .search-input,
                        .search-btn {
                            border: none;
                            outline: none;
                            background: transparent;
                            height: 24px;
                            line-height: 24px;
                        }
                        .search-btn {
                            color: var(--main-header-bgckground);
                        }

                        .search-input:focus {
                            outline: none;
                        }
                    }

                    li:last-child {
                        margin-right: 0;
                    }
                }
            }
        }

        .ms300 {
            transition: all 300ms ease;
        }

        .ms200 {
            transition: all 200ms ease;
        }

        .adTxt {
            margin: 0px 30px;
            min-width: 150px;
            max-width: 300px;
            overflow: hidden;
        }

        .main-box {
            width: 100%;
            height: 88px;
            background: #ffffff;
            box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);

            .logo-box {
                float: left;
                padding-top: 16px;
                padding-bottom: 5px;

                .logo {
                    line-height: 60px;
                    font-size: 28px;
                    a {
                        color: var(--main-header-bgckground);
                    }
                }

                .logo img {
                    display: inline-block;
                    max-width: 100%;
                }
            }

            .main-menu {
                float: right;

                .navigation {
                    > li {
                        float: left;
                        display: inline;
                        padding: 34px 25px 22px 33px;
                        margin-left: -4px;
                        background: url(@/assets/images/top-nav-bg.png) left 40px no-repeat;

                        > a {
                            position: relative;
                            display: block;
                            overflow: hidden;
                            font-size: 16px;
                            height: 24px;
                            color: #111111;
                            line-height: 24px;
                            text-transform: uppercase;

                            > span {
                                display: block;
                                margin-top: 0;

                                em {
                                    color: var(--main-header-bgckground, #5abdcb);
                                    font-style: normal;
                                }
                            }
                        }
                    }

                    > li:first-child {
                        background: none;
                    }

                    > li:last-child {
                        padding-right: 10px;
                    }

                    > li:hover > a > span {
                        margin-top: -24px;
                    }
                }

                /* 子菜单 */
                div.sub-menu {
                    position: absolute;
                    left: 0;
                    right: 0;
                    margin-top: 15px;
                    overflow: hidden;
                    z-index: 100000;
                    opacity: 0;
                    visibility: hidden;
                    background: #f5f5f5;
                    transition: all 600ms ease;

                    .items {
                        overflow: hidden;
                        width: 1400px;
                        padding: 30px 10px;
                        margin: 0 auto;
                        display: flex;
                        flex-wrap: wrap;

                        .item {
                            width: 33.333%;
                            border-left: 1px solid #ddd;
                            border-right: 1px solid #ddd;
                            /*&.item:nth-child(3n), &.item:last-child{
                                border-right: 1px solid #dddddd;
                            }*/
                            a {
                                padding: 13px 0;
                                display: block;
                                text-align: center;
                                font-size: 18px;
                                color: #444;
                            }

                            a:hover {
                                transform: translateY(-5px);
                                color: var(--main-header-bgckground);
                            }
                        }
                    }
                }

                .navigation > li:hover > div.sub-menu {
                    opacity: 1;
                    visibility: visible;
                }
            }

            .nav-toggler {
                float: right;
                margin-top: 16px;
                display: none;
            }
        }
    }

    .main-header.main-header-fixed {
        .main-box {
            position: fixed;
            left: 0;
            top: 0;
            width: 100%;
            background: #FFFFFF;
            z-index: 10000;
        }
    }

    @media screen and (max-width: 900px) {
        .main-header {
            height: auto;
            .auto-1400,
            .auto-1200 {
                width: 96%;
                padding: 0 2%;
            }

            .main-box .logo-box {
                padding-top: 10px;
            }

            .mobile {
                display: block;
            }
            .mobile.mobile-mask {
                visibility: hidden;
                position: fixed;
                left: 0;
                top: 0;
                width: 100vw;
                height: 100vh;
                opacity: 0;
                background: rgba(0, 0, 0, 0.5);
                z-index: 100;
                transition: opacity 0.3s ease;
            }

            .talkerMenu {
                margin-top: 0px;
                top: unset;
                bottom: 5%;
                -webkit-transform: scale(0.5);
                -moz-transform: scale(0.5);
                transform: scale(0.5);
            }

            .talkerMenu ul li.qqicon,
            .talkerMenu ul li.wxicon {
                display: none;
            }

            /*.main-header .header-top {padding-bottom:10px;}
            .main-header .header-top .top-left {clear:both;width:100%;text-align:center;}
            .main-header .header-top .top-right ul li {width:32%;text-align:center;margin-left:0;margin-right:0;font-size:12px;}
            .main-header .header-top .top-right ul li .aicf {display:none;}
            .main-header .header-top .top-right ul li.sli {width:45%;padding:0;margin-left:3%;}*/
            /*.main-header .header-top { margin-top: -110px;}*/

            .adTxt {
                display: none;
            }

            .nav-toggler {
                display: block !important;

                .hidden-bar-opener {
                    position: relative;
                    display: block;
                    height: 36px;
                    width: 40px;
                    background: #5abdcb;
                    color: #ffffff;
                    text-align: center;
                    font-size: 18px;
                    line-height: 34px;
                    border: 1px solid #5abdcb;
                    border-radius: 3px;
                    font-weight: normal;
                }
            }

            .header-top {
                display: none;
            }

            .main-box {
                .main-menu {
                    position: fixed;
                    top: 0;
                    right: -305px;
                    width: 305px;
                    bottom: 0;
                    background: #272727;
                    z-index: 9999;
                    display: block;
                    padding-top: 30px;
                    .hidden-bar-closer {
                        position: absolute;
                        z-index: 1;
                        top: 0;
                        width: 100%;
                        height: 20px;
                        background: rgba(255, 255, 255, 0.2);
                        border-radius: 2px;
                        line-height: 20px;
                        color: #fff;
                        text-align: center;
                        font-size: 12px;
                    }
                    .navigation {
                        display: flex;
                        flex-direction: column;
                        > li {
                            padding: 0;
                            line-height: 40px;
                            border-bottom: 1px solid #666;
                            margin-left: 0;
                            background: transparent;
                            > a {
                                position: relative;
                                display: block;
                                overflow: hidden;
                                font-size: 16px;
                                height: 48px;
                                color: #fff;
                                line-height: 48px;
                                text-transform: uppercase;
                                padding-left: 25px;
                                > .aicf {
                                    position: absolute;
                                    right: 0;
                                    top: 0;
                                    width: 48px;
                                    height: 48px;
                                    text-align: center;
                                    line-height: 48px;
                                }
                                span {
                                    display: block;
                                    margin-top: 0;
                                    padding-left: 2em;
                                    em {
                                        color: #fc721e;
                                        font-style: normal;
                                    }
                                }
                            }
                            .sub-menu {
                                display: none;
                                border-top: 1px solid #444;
                            }
                            .items {
                                clear: both;
                                width: 100%;
                                overflow: hidden;
                                > div.img {
                                    display: none;
                                }
                                a {
                                    color: #fff;
                                    line-height: 48px;
                                    display: block;
                                    text-indent: 4em;
                                    font-size: 14px;
                                    .aicf {
                                        margin-right: 5px;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        .main-header.hover {
            .main-box {
                .main-menu {
                    right: 0px;
                    animation: fadeInRight 300ms;
                    .mobile-close {
                        position: absolute;
                        right: 5px;
                        top: 5px;
                        width: 35px;
                        height: 35px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        background: #FFFFFF;
                        border-radius: 50%;
                    }
                }
            }
            .mobile.mobile-mask {
                opacity: 1;
                visibility: visible;
            }
        }
    }
</style>
