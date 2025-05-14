export default [
    {
        label: "课程管理",
        to: "",
        children: [
            {
                label: "发布课程",
                to: { path: "/admin/kechengxinxi/add" },
            },
            {
                label: "课程查询",
                to: { path: "/admin/kechengxinxi/fabujiaoshi" },
            },
            {
                label: "课程视频查询",
                to: { path: "/admin/kechengshipin/fabujiaoshi" },
            },
            {
                label: "课程资源查询",
                to: { path: "/admin/kechengziyuan/fabujiaoshi" },
            },
        ],
    },
    {
        label: "课程学习管理",
        to: "",
        children: [
            {
                label: "课程学习查询",
                to: { path: "/admin/kechengxuexi/fabujiaoshi" },
            },
            {
                label: "学习进度查询",
                to: { path: "/admin/xuexijindu/fabujiaoshi" },
            },
            {
                label: "学习记录查询",
                to: { path: "/admin/xuexijilu/fabujiaoshi" },
            },
        ],
    },
    {
        label: "布置作业管理",
        to: "",
        children: [
            {
                label: "布置作业查询",
                to: { path: "/admin/buzhizuoye/fabujiaoshi" },
            },
            {
                label: "提交作业查询",
                to: { path: "/admin/tijiaozuoye/fabujiaoshi" },
            },
            {
                label: "作业批阅查询",
                to: { path: "/admin/zuoyepiyue/fabujiaoshi" },
            },
        ],
    },
    {
        label: "个人中心",
        to: "",
        children: [
            {
                label: "修改个人资料",
                to: { path: "/admin/jiaoshi/updtself" },
            },
            {
                label: "修改密码",
                to: { path: "/admin/mod" },
            },
            /*{
                label: "我的收藏",
                to: { path: "/admin/shoucang/username" },
            },*/
        ],
    },
];
