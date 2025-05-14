import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores";
import routes from "./routes";
import config from "@/config";
import { ElMessageBox } from "element-plus";
import { inArray } from "@/utils";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

router.beforeEach(async (to, from, next) => {
    var user = useUserStore();
    if (to.meta.authLogin) {
        // 需要验证登录
        if (!user.isLogin()) {
            // 学习路径路由特殊处理
            if (to.path === '/learning-path') {
                await ElMessageBox.alert("请先登录后再访问学习路径", "提示", {
                    confirmButtonText: "确定",
                    type: "warning"
                });
                return next('/index');
            } else if (to.meta.msg) {
                await ElMessageBox.alert("尚未登录，请登录后操作");
            }
            return next(`/login?redirect=${to.fullPath}`);
        }
    }

    document.title = (to.meta.title ? to.meta.title + "-" : "") + config.title;
    next();
});

// 添加全局错误处理
router.onError((error) => {
    console.error('路由错误:', error);
    
    // 检查是否是动态导入模块失败
    if (error.message.includes('Failed to fetch dynamically imported module')) {
        // 尝试简单的页面刷新
        console.log('尝试通过刷新页面解决模块加载问题');
        
        // 记录当前路径，以便刷新后重定向回来
        const currentPath = router.currentRoute.value.fullPath;
        localStorage.setItem('last_route_error_path', currentPath);
        localStorage.setItem('last_route_error_time', Date.now());
        
        // 只有在非连续错误的情况下自动刷新
        const lastErrorTime = parseInt(localStorage.getItem('last_route_error_time') || '0');
        if (Date.now() - lastErrorTime > 10000) { // 10秒内不重复刷新
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            ElMessageBox.alert("页面加载失败，请手动刷新页面或重新登录。", "加载错误", {
                confirmButtonText: "刷新",
                callback: () => {
                    window.location.reload();
                }
            });
        }
    } else {
        // 显示通用的错误提示
        ElMessageBox.alert("页面加载失败，请刷新重试", "错误", {
            confirmButtonText: "确定"
        });
    }
});

export default router;

