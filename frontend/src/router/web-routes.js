import { session } from "@/utils/utils";
export default [
    {
        path: "xuesheng/add",
        name: "IndexxueshengAdd",
        component: () => import("@/views/xuesheng/add-web.vue"),
        meta: { title: "学生添加" },
    },
    {
        path: "shoucang/add",
        name: "IndexshoucangAdd",
        component: () => import("@/views/shoucang/add-web.vue"),
        meta: { title: "收藏添加", authLogin: true, msg: true },
    },
    {
        path: "siliao/add",
        name: "IndexsiliaoAdd",
        component: () => import("@/views/siliao/add-web.vue"),
        meta: { title: "私聊添加", authLogin: true, msg: true },
    },
    {
        path: "luntanjiaoliu",
        name: "IndexluntanjiaoliuList",
        component: () => import("@/views/luntanjiaoliu/index.vue"),
        meta: { title: "论坛交流列表" },
    },
    {
        path: "luntanjiaoliu/detail",
        name: "IndexluntanjiaoliuDetail",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/luntanjiaoliu/detail-web.vue"),
        meta: { title: "论坛交流详情" },
    },
    {
        path: "jiaoliuhuifu/add",
        name: "IndexjiaoliuhuifuAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/jiaoliuhuifu/add-web.vue"),
        meta: { title: "交流回复添加", authLogin: true, msg: true },
    },
    {
        path: "jiaoshi/add",
        name: "IndexjiaoshiAdd",
        component: () => import("@/views/jiaoshi/add-web.vue"),
        meta: { title: "教师添加" },
    },
    {
        path: "kechengxinxi",
        name: "IndexkechengxinxiList",
        component: () => import("@/views/kechengxinxi/index.vue"),
        meta: { title: "课程信息列表" },
    },
    {
        path: "kechengxinxi/detail",
        name: "IndexkechengxinxiDetail",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengxinxi/detail-web.vue"),
        meta: { title: "课程信息详情" },
    },
    {
        path: "kechengshipin/detail",
        name: "IndexkechengshipinDetail",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengshipin/detail-web.vue"),
        meta: { title: "课程视频详情", authLogin: true, msg: true },
    },
    {
        path: "kechengxuexi/add",
        name: "IndexkechengxuexiAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengxuexi/add-web.vue"),
        meta: { title: "课程学习添加", authLogin: true, msg: true },
    },
    {
        path: "buzhizuoye/detail",
        name: "IndexbuzhizuoyeDetail",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/buzhizuoye/detail-web.vue"),
        meta: { title: "布置作业详情", authLogin: true, msg: true },
    },
    {
        path: "tijiaozuoye/add",
        name: "IndextijiaozuoyeAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/tijiaozuoye/add-web.vue"),
        meta: { title: "提交作业添加", authLogin: true, msg: true },
    },
    {
        path: "zhinengwenda",
        name: "Zhinengwenda",
        component: () => import("@/views/zhinengwenda/index.vue"),
        meta: { title: "智能问答", authLogin: true },
    },
    {
        path: "xuexifenxi",
        name: "Xuexifenxi",
        component: () => {
            try {
                console.log('Attempting to load xuexifenxi component...');
                return import("@/views/xuexifenxi/index.vue").catch(error => {
                    console.error('Failed to load xuexifenxi component:', error);
                    return import("@/views/ErrorPage.vue");
                });
            } catch (error) {
                console.error('Error in the dynamic import itself:', error);
                return import("@/views/ErrorPage.vue");
            }
        },
        meta: { title: "学习分析", authLogin: true },
    },
    {
        path: "learning-path",
        name: "LearningPath",
        component: () => import("@/views/LearningPath.vue"),
        meta: { title: "学习路径", authLogin: true }
    }
];
