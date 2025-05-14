import config from "@/config";
import { isFunction, isObject, isArray } from "@/utils/extend";
import http from "@/utils/ajax/http";
import { ElMessage, ElMessageBox, ElLoading } from "element-plus";
import { useUserStore } from "@/stores";
import router from "@/router";
import { unref } from "vue";

export function formatImageSrc(value) {
    if (!value) return "";
    if (value instanceof Blob) {
        return value;
    }
    if (value.indexOf("data:image") === 0) {
        return value;
    }
    if (value.indexOf("/") === 0) {
        return config.service_url + value;
    }
    var url = value;
    if (!url.match(/^https?:\/\//gi)) {
        return config.service_url + "/" + value;
    }
    return url;
}

export function session(name) {
    try {
        var user = useUserStore();
        
        // 检查用户是否已登录
        const isLoggedIn = user.isLogin();
        console.log(`session('${name}') 调用，用户登录状态:`, isLoggedIn);
        
        if (!isLoggedIn) {
            console.warn(`尝试获取 session('${name}') 但用户未登录`);
            return null;
        }
        
        // 获取会话数据
        const value = user.getSession(name);
        console.log(`session('${name}') 返回值:`, value);
        
        return value;
    } catch (error) {
        console.error(`获取session('${name}')时发生错误:`, error);
        return null;
    }
}

export function logout() {
    // 确保UI一致性和良好的用户体验
    ElMessageBox.confirm("您确定要退出登录吗？", "退出登录", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        roundButton: true,
    }).then(async () => {
        try {
            // 显示加载状态
            const loadingInstance = ElLoading.service({
                lock: true,
                text: '正在退出登录...',
                background: 'rgba(0, 0, 0, 0.7)'
            });
            
            // 获取用户store
            const userStore = useUserStore();
            
            // 执行退出前先记录状态
            console.log('开始退出登录流程');
            
            try {
                // 设置超时，确保即使后端无响应也能完成退出
                const logoutPromise = userStore.logout();
                const timeoutPromise = new Promise((resolve) => {
                    setTimeout(() => resolve({ code: 0, msg: '退出登录超时，已本地处理' }), 5000);
                });
                
                // 等待退出请求完成或超时
                await Promise.race([logoutPromise, timeoutPromise]);
                
                // 关闭加载提示
                loadingInstance.close();
                
                // 显示成功消息
                ElMessage.success({
                    message: "退出登录成功",
                    duration: 2000
                });
                
                // 等待消息显示后再刷新页面
                setTimeout(() => {
                    // 根据路由配置跳转到合适的页面
                    if (router.hasRoute("Index")) {
                        router.replace({
                            path: '/refresh',
                            query: { redirect: '/index' }
                        });
                    } else {
                        router.replace({
                            path: '/refresh',
                            query: { redirect: '/login' }
                        });
                    }
                }, 500);
                
            } catch (err) {
                // 关闭加载提示
                loadingInstance.close();
                
                console.error("退出登录请求失败:", err);
                
                // 显示警告但仍然清除本地状态
                ElMessage.warning({
                    message: "网络请求失败，但已清除本地登录状态",
                    duration: 3000
                });
                
                // 强制清除本地状态
                userStore.setToken(null);
                userStore.setSession(null);
                userStore.setRoles(null);
                
                // 等待消息显示后刷新页面
                setTimeout(() => {
                    if (router.hasRoute("Index")) {
                        router.replace({
                            path: '/refresh',
                            query: { redirect: '/index' }
                        });
                    } else {
                        router.replace({
                            path: '/refresh',
                            query: { redirect: '/login' }
                        });
                    }
                }, 1000);
            }
        } catch (err) {
            console.error("退出登录过程出错:", err);
            ElMessage.error("退出登录失败，请刷新页面后重试");
        }
    }).catch(() => {
        console.log("用户取消退出登录");
    });
}

export function remove(arr, key) {
    if (isObject(key) || isArray(key)) {
        var index = findIndex(arr, (r) => r === key);
        if (index !== false) {
            remove(arr, index);
        }
    } else {
        if (isObject(arr)) {
            delete arr[key];
        } else {
            arr.splice(key, 1);
        }
    }
}

export function checkIssh(row, module) {
    http.post(config.checkUpdate, {
        tablename: module,
        id: row.id,
        yuan: row.issh,
    }).then(
        (res) => {
            if (res.code == 0) {
                row.issh = row.issh == "是" ? "否" : "是";
            } else {
                ElMessage.error(res.msg);
            }
        },
        (err) => {
            ElMessage.error(err.message);
        }
    );
}

export function findIndex(arr, callback) {
    if (!isFunction(callback)) {
        throw new Error("findObject第二个参数是回调函数");
    }
    for (var i in arr) {
        var ci = arr[i];
        if (callback(ci, i)) {
            return i;
        }
    }
    return false;
}

export function findObject(arr, callback) {
    if (!isFunction(callback)) {
        throw new Error("findObject第二个参数是回调函数");
    }
    for (var i in arr) {
        var ci = arr[i];
        if (callback(ci, i)) {
            return ci;
        }
    }
    return false;
}

export function upload(file) {
    return new Promise((resolve, reject) => {
        var formdata = new FormData();
        formdata.append("fujian", file, file.name || "tmp.png");
        http.post(config.uploadUrl, formdata)
            .then((res) => {
                if (res.code == 0) {
                    resolve(res.data);
                } else {
                    reject(res.msg);
                }
            })
            .catch((err) => {
                reject(err.message);
            });
    });
}

export function formatHtml(html) {
    var regex = /(<([^>]+)>)/gi;
    return html.replace(regex, "");
}

export function substr(str, length, append = "...") {
    if (!str) return "";
    var s = formatHtml(unref(str));
    if (s.length > length) {
        return s.substr(0, length) + append;
    }
    return s;
}

export function captch() {
    return new Promise((resolve, reject) => {
        const params = { rand: Math.floor(Math.random() * 10000) };
        
        http.get(config.captch_url, params).then(
            (res) => {
                // 直接检查响应对象中的token和url
                if (res && (res.token || (res.data && res.data.token))) {
                    const data = res.data || res;
                    resolve(data);
                } else if (res.code == 0) {
                    // 检查响应数据的完整性
                    if (!res.data) {
                        reject('验证码响应数据为空');
                        return;
                    }
                    
                    // 检查token和url是否存在
                    if (!res.data.token || !res.data.url) {
                        reject('验证码数据不完整');
                        return;
                    }
                    
                    resolve(res.data);
                } else {
                    ElMessage.error(res.msg || '验证码获取失败');
                    reject(res.msg || '验证码获取失败');
                }
            },
            (err) => {
                reject(err.message || '网络请求失败');
            }
        );
    });
}

export function downloadFile(fileRealPath, fileName) {
    let link = document.createElement("a");
    let url = fileRealPath; //codeIMG  要下载的路径
    // 这里是将url转成blob地址，
    http.get(url).thenBlob((blob) => {
        // 将链接地址字符内容转变成blob地址
        link.href = window.URL.createObjectURL(blob);
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(link.href);
    });
}

export default {
    findIndex,
    findObject,
    formatImageSrc,
    checkIssh,
    remove,
    logout,
    session,
    downloadFile,
    captch,
};
