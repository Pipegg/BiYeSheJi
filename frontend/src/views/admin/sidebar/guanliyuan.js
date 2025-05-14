export default [
    {
        label: "账号管理",
        to: "",
        children: [
            {
                label: "管理员账号管理",
                to: { path: "/admin/admins" },
            },
            {
                label: "管理员账号添加",
                to: { path: "/admin/admins/add" },
            },
            {
                label: "密码修改",
                to: { path: "/admin/mod" },
            },
        ],
    },
    {
        label: "学生管理",
        to: "",
        children: [
            {
                label: "学生查询",
                to: { path: "/admin/xuesheng" },
            },
        ],
    },
    {
        label: "教师管理",
        to: "",
        children: [
            {
                label: "教师添加",
                to: { path: "/admin/jiaoshi/add" },
            },
            {
                label: "教师查询",
                to: { path: "/admin/jiaoshi" },
            },
        ],
    },
    {
        label: "论坛交流管理",
        to: "",
        children: [
            {
                label: "论坛分类添加",
                to: { path: "/admin/luntanfenlei/add" },
            },
            {
                label: "论坛分类查询",
                to: { path: "/admin/luntanfenlei" },
            },
            {
                label: "论坛交流查询",
                to: { path: "/admin/luntanjiaoliu" },
            },
            {
                label: "交流回复查询",
                to: { path: "/admin/jiaoliuhuifu" },
            },
        ],
    },
    {
        label: "课程信息管理",
        to: "",
        children: [
            {
                label: "课程分类添加",
                to: { path: "/admin/kechengfenlei/add" },
            },
            {
                label: "课程分类查询",
                to: { path: "/admin/kechengfenlei" },
            },
            {
                label: "课程信息查询",
                to: { path: "/admin/kechengxinxi" },
            },
            {
                label: "课程视频查询",
                to: { path: "/admin/kechengshipin" },
            },
            {
                label: "课程资源查询",
                to: { path: "/admin/kechengziyuan" },
            },
        ],
    },
    {
        label: "课程学习管理",
        to: "",
        children: [
            {
                label: "课程学习查询",
                to: { path: "/admin/kechengxuexi" },
            },
            {
                label: "学习进度查询",
                to: { path: "/admin/xuexijindu" },
            },
            {
                label: "学习记录查询",
                to: { path: "/admin/xuexijilu" },
            },
        ],
    },
    {
        label: "布置作业管理",
        to: "",
        children: [
            {
                label: "布置作业查询",
                to: { path: "/admin/buzhizuoye" },
            },
            {
                label: "提交作业查询",
                to: { path: "/admin/tijiaozuoye" },
            },
            {
                label: "作业批阅查询",
                to: { path: "/admin/zuoyepiyue" },
            },
        ],
    },
    {
        label: "问答管理",
        to: "",
        children: [
            {
                label: "问答添加",
                to: { path: "/admin/wenda/add" },
            },
            {
                label: "问答查询",
                to: { path: "/admin/wenda" },
            },
            {
                label: "回答添加",
                to: { path: "/admin/huida/add" },
            },
            {
                label: "回答查询",
                to: { path: "/admin/huida" },
            },
            {
                label: "问答消息查询",
                to: { path: "/admin/wendaxiaoxi" },
            },
        ],
    },

    {
        label: "系统管理",
        to: "",
        children: [
            {
                label: "友情链接添加",
                to: { path: "/admin/youqinglianjie/add" },
            },
            {
                label: "友情链接查询",
                to: { path: "/admin/youqinglianjie" },
            },
            {
                label: "轮播图添加",
                to: { path: "/admin/lunbotu/add" },
            },
            {
                label: "轮播图查询",
                to: { path: "/admin/lunbotu" },
            },
        ],
    },
];
