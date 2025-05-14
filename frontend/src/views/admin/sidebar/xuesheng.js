export default [
    {
        label: "智能学习助手",
        to: "",
        children: [
            {
                label: "智能问答",
                to: { path: "/zhinengwenda" },
            },
            {
                label: "学习分析",
                to: { path: "/xuexifenxi" },
            },
        ],
    },
    {
        label: "论坛交流管理",
        to: "",
        children: [
            {
                label: "发布论坛",
                to: { path: "/admin/luntanjiaoliu/add" },
            },
            {
                label: "查看论坛",
                to: { path: "/admin/luntanjiaoliu/faburen" },
            },
            {
                label: "交流回复查询",
                to: { path: "/admin/jiaoliuhuifu/huifuren" },
            },
        ],
    },
    {
        label: "课程学习管理",
        to: "",
        children: [
            {
                label: "课程学习查询",
                to: { path: "/admin/kechengxuexi/xueshengyonghu" },
            },
            {
                label: "学习进度查询",
                to: { path: "/admin/xuexijindu/xueshengyonghu" },
            },
        ],
    },
    {
        label: "学习记录管理",
        to: "",
        children: [
            {
                label: "学习记录查询",
                to: { path: "/admin/xuexijilu/xueshengyonghu" },
            },
        ],
    },
    {
        label: "布置作业管理",
        to: "",
        children: [
          /*  {
                label: "布置作业查询",
                to: { path: "/admin/buzhizuoye" },
            },*/
            {
                label: "提交作业查询",
                to: { path: "/admin/tijiaozuoye/tijiaoxuesheng" },
            },
            {
                label: "作业批阅查询",
                to: { path: "/admin/zuoyepiyue/tijiaoxuesheng" },
            },
        ],
    },
    {
        label: "个人中心",
        to: "",
        children: [
            {
                label: "修改个人资料",
                to: { path: "/admin/xuesheng/updtself" },
            },
            {
                label: "修改密码",
                to: { path: "/admin/mod" },
            },
            {
                label: "我的收藏",
                to: { path: "/admin/shoucang/username" },
            },
        ],
    },
];
