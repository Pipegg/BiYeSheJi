import WebRoutes from "./web-routes";

import AdminRoutes from "./admin-routes";

const routes = [
    {
        path: "/",
        name: "Home",
        component: () => import("@/views/home.vue"),
        redirect: "/index",
        meta: { title: "" },
        children: [
            {
                path: "index",
                name: "Index",
                component: () => import("@/views/index.vue"),
                meta: { title: "首页" },
            },
            ...WebRoutes,
        ],
    },

    {
        path: "/login",
        name: "Login",
        component: () => import("@/views/login/index.vue"),
        meta: { title: "系统登录" },
    },
    {
        path: "/refresh",
        name: "Refresh",
        component: () => import("@/views/index.vue"),
        beforeEnter: (to, from, next) => {
            const { redirect } = to.query;
            if (redirect) {
                next(redirect);
            } else {
                next('/index');
            }
        },
        meta: { title: "刷新中..." },
    },
    {
        path: "/admin",
        name: "Admin",
        component: () => import("@/views/admin/index.vue"),
        redirect: "/login",
        meta: { title: "后台管理", authLogin: true },
        children: [
            {
                path: "sy",
                name: "AdminSy",
                component: () => import("@/views/admin/sy.vue"),
                meta: { authLogin: true, title: "欢迎页", affix: true },
            },
            {
                path: "mod",
                name: "AdminMod",
                component: () => import("@/views/admin/mod.vue"),
                meta: { authLogin: true, title: "修改密码" },
            },
            ...AdminRoutes,
        ],
    },
    {
        path: '/recommendations',
        name: 'CourseRecommendations',
        component: () => import("@/components/CourseRecommendation.vue"),
        meta: {
            title: '课程推荐',
            requiresAuth: true
        }
    },
];

export default routes;
