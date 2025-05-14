import { session } from "@/utils/utils";

export default [
    {
        path: "admins",
        name: "AdminadminsList",
        component: () => import("@/views/admins/list.vue"),
        meta: { title: "管理员列表", authLogin: true },
    },

    {
        path: "admins/add",
        name: "AdminadminsAdd",
        component: () => import("@/views/admins/add.vue"),
        meta: { title: "添加管理员", authLogin: true },
    },
    {
        path: "admins/updt",
        name: "AdminadminsUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/admins/updt.vue"),
        meta: { title: "编辑管理员", authLogin: true },
    },
    {
        path: "admins/updtself",
        name: "AdminadminsUpdtSelf",
        props: (route) => ({ id: session("id") }),
        component: () => import("@/views/admins/updtself.vue"),
        meta: { title: "更新个人资料", authLogin: true },
    },
    {
        path: "admins/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminadminsDetail",
        component: () => import("@/views/admins/detail.vue"),
        meta: { title: "管理员详情", authLogin: true },
    },
    {
        path: "xuesheng",
        name: "AdminxueshengList",
        component: () => import("@/views/xuesheng/list.vue"),
        meta: { title: "学生列表", authLogin: true },
    },

    {
        path: "xuesheng/add",
        name: "AdminxueshengAdd",
        component: () => import("@/views/xuesheng/add.vue"),
        meta: { title: "添加学生", authLogin: true },
    },
    {
        path: "xuesheng/updt",
        name: "AdminxueshengUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xuesheng/updt.vue"),
        meta: { title: "编辑学生", authLogin: true },
    },
    {
        path: "xuesheng/updtself",
        name: "AdminxueshengUpdtSelf",
        props: (route) => ({ id: session("id") }),
        component: () => import("@/views/xuesheng/updtself.vue"),
        meta: { title: "更新个人资料", authLogin: true },
    },
    {
        path: "xuesheng/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminxueshengDetail",
        component: () => import("@/views/xuesheng/detail.vue"),
        meta: { title: "学生详情", authLogin: true },
    },
    {
        path: "youqinglianjie",
        name: "AdminyouqinglianjieList",
        component: () => import("@/views/youqinglianjie/list.vue"),
        meta: { title: "友情链接列表", authLogin: true },
    },

    {
        path: "youqinglianjie/add",
        name: "AdminyouqinglianjieAdd",
        component: () => import("@/views/youqinglianjie/add.vue"),
        meta: { title: "添加友情链接", authLogin: true },
    },
    {
        path: "youqinglianjie/updt",
        name: "AdminyouqinglianjieUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/youqinglianjie/updt.vue"),
        meta: { title: "编辑友情链接", authLogin: true },
    },
    {
        path: "lunbotu",
        name: "AdminlunbotuList",
        component: () => import("@/views/lunbotu/list.vue"),
        meta: { title: "轮播图列表", authLogin: true },
    },

    {
        path: "lunbotu/add",
        name: "AdminlunbotuAdd",
        component: () => import("@/views/lunbotu/add.vue"),
        meta: { title: "添加轮播图", authLogin: true },
    },
    {
        path: "lunbotu/updt",
        name: "AdminlunbotuUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/lunbotu/updt.vue"),
        meta: { title: "编辑轮播图", authLogin: true },
    },
    {
        path: "shoucang",
        name: "AdminshoucangList",
        component: () => import("@/views/shoucang/list.vue"),
        meta: { title: "收藏列表", authLogin: true },
    },

    {
        path: "shoucang/username",
        name: "AdminshoucangListusername",
        component: () => import("@/views/shoucang/username.vue"),
        meta: { title: "收藏列表", authLogin: true },
    },

    {
        path: "siliao",
        name: "AdminsiliaoList",
        component: () => import("@/views/siliao/list.vue"),
        meta: { title: "私聊列表", authLogin: true },
    },

    {
        path: "siliao/shouxinren",
        name: "AdminsiliaoListshouxinren",
        component: () => import("@/views/siliao/shouxinren.vue"),
        meta: { title: "私聊列表", authLogin: true },
    },
    {
        path: "siliao/faxinren",
        name: "AdminsiliaoListfaxinren",
        component: () => import("@/views/siliao/faxinren.vue"),
        meta: { title: "私聊列表", authLogin: true },
    },

    {
        path: "siliao/add",
        name: "AdminsiliaoAdd",
        component: () => import("@/views/siliao/add.vue"),
        meta: { title: "添加私聊", authLogin: true },
    },
    {
        path: "siliao/updt",
        name: "AdminsiliaoUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/siliao/updt.vue"),
        meta: { title: "编辑私聊", authLogin: true },
    },
    {
        path: "xiaoxi",
        name: "AdminxiaoxiList",
        component: () => import("@/views/xiaoxi/list.vue"),
        meta: { title: "消息列表", authLogin: true },
    },

    {
        path: "xiaoxi/fasongren",
        name: "AdminxiaoxiListfasongren",
        component: () => import("@/views/xiaoxi/fasongren.vue"),
        meta: { title: "消息列表", authLogin: true },
    },

    {
        path: "xiaoxi/add",
        name: "AdminxiaoxiAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xiaoxi/add.vue"),
        meta: { title: "添加消息", authLogin: true },
    },
    {
        path: "xiaoxi/updt",
        name: "AdminxiaoxiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xiaoxi/updt.vue"),
        meta: { title: "编辑消息", authLogin: true },
    },
    {
        path: "luntanjiaoliu",
        name: "AdminluntanjiaoliuList",
        component: () => import("@/views/luntanjiaoliu/list.vue"),
        meta: { title: "论坛交流列表", authLogin: true },
    },

    {
        path: "luntanjiaoliu/faburen",
        name: "AdminluntanjiaoliuListfaburen",
        component: () => import("@/views/luntanjiaoliu/faburen.vue"),
        meta: { title: "论坛交流列表", authLogin: true },
    },

    {
        path: "luntanjiaoliu/add",
        name: "AdminluntanjiaoliuAdd",
        component: () => import("@/views/luntanjiaoliu/add.vue"),
        meta: { title: "添加论坛交流", authLogin: true },
    },
    {
        path: "luntanjiaoliu/updt",
        name: "AdminluntanjiaoliuUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/luntanjiaoliu/updt.vue"),
        meta: { title: "编辑论坛交流", authLogin: true },
    },
    {
        path: "luntanjiaoliu/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminluntanjiaoliuDetail",
        component: () => import("@/views/luntanjiaoliu/detail.vue"),
        meta: { title: "论坛交流详情", authLogin: true },
    },
    {
        path: "luntanfenlei",
        name: "AdminluntanfenleiList",
        component: () => import("@/views/luntanfenlei/list.vue"),
        meta: { title: "论坛分类列表", authLogin: true },
    },

    {
        path: "luntanfenlei/add",
        name: "AdminluntanfenleiAdd",
        component: () => import("@/views/luntanfenlei/add.vue"),
        meta: { title: "添加论坛分类", authLogin: true },
    },
    {
        path: "luntanfenlei/updt",
        name: "AdminluntanfenleiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/luntanfenlei/updt.vue"),
        meta: { title: "编辑论坛分类", authLogin: true },
    },
    {
        path: "jiaoliuhuifu",
        name: "AdminjiaoliuhuifuList",
        component: () => import("@/views/jiaoliuhuifu/list.vue"),
        meta: { title: "交流回复列表", authLogin: true },
    },

    {
        path: "jiaoliuhuifu/faburen",
        name: "AdminjiaoliuhuifuListfaburen",
        component: () => import("@/views/jiaoliuhuifu/faburen.vue"),
        meta: { title: "交流回复列表", authLogin: true },
    },
    {
        path: "jiaoliuhuifu/huifuren",
        name: "AdminjiaoliuhuifuListhuifuren",
        component: () => import("@/views/jiaoliuhuifu/huifuren.vue"),
        meta: { title: "交流回复列表", authLogin: true },
    },

    {
        path: "jiaoliuhuifu/add",
        name: "AdminjiaoliuhuifuAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/jiaoliuhuifu/add.vue"),
        meta: { title: "添加交流回复", authLogin: true },
    },
    {
        path: "jiaoliuhuifu/updt",
        name: "AdminjiaoliuhuifuUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/jiaoliuhuifu/updt.vue"),
        meta: { title: "编辑交流回复", authLogin: true },
    },
    {
        path: "jiaoliuhuifu/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminjiaoliuhuifuDetail",
        component: () => import("@/views/jiaoliuhuifu/detail.vue"),
        meta: { title: "交流回复详情", authLogin: true },
    },
    {
        path: "jiaoshi",
        name: "AdminjiaoshiList",
        component: () => import("@/views/jiaoshi/list.vue"),
        meta: { title: "教师列表", authLogin: true },
    },

    {
        path: "jiaoshi/add",
        name: "AdminjiaoshiAdd",
        component: () => import("@/views/jiaoshi/add.vue"),
        meta: { title: "添加教师", authLogin: true },
    },
    {
        path: "jiaoshi/updt",
        name: "AdminjiaoshiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/jiaoshi/updt.vue"),
        meta: { title: "编辑教师", authLogin: true },
    },
    {
        path: "jiaoshi/updtself",
        name: "AdminjiaoshiUpdtSelf",
        props: (route) => ({ id: session("id") }),
        component: () => import("@/views/jiaoshi/updtself.vue"),
        meta: { title: "更新个人资料", authLogin: true },
    },
    {
        path: "jiaoshi/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminjiaoshiDetail",
        component: () => import("@/views/jiaoshi/detail.vue"),
        meta: { title: "教师详情", authLogin: true },
    },
    {
        path: "kechengfenlei",
        name: "AdminkechengfenleiList",
        component: () => import("@/views/kechengfenlei/list.vue"),
        meta: { title: "课程分类列表", authLogin: true },
    },

    {
        path: "kechengfenlei/add",
        name: "AdminkechengfenleiAdd",
        component: () => import("@/views/kechengfenlei/add.vue"),
        meta: { title: "添加课程分类", authLogin: true },
    },
    {
        path: "kechengfenlei/updt",
        name: "AdminkechengfenleiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengfenlei/updt.vue"),
        meta: { title: "编辑课程分类", authLogin: true },
    },
    {
        path: "kechengxinxi",
        name: "AdminkechengxinxiList",
        component: () => import("@/views/kechengxinxi/list.vue"),
        meta: { title: "课程信息列表", authLogin: true },
    },

    {
        path: "kechengxinxi/fabujiaoshi",
        name: "AdminkechengxinxiListfabujiaoshi",
        component: () => import("@/views/kechengxinxi/fabujiaoshi.vue"),
        meta: { title: "课程信息列表", authLogin: true },
    },

    {
        path: "kechengxinxi/add",
        name: "AdminkechengxinxiAdd",
        component: () => import("@/views/kechengxinxi/add.vue"),
        meta: { title: "添加课程信息", authLogin: true },
    },
    {
        path: "kechengxinxi/updt",
        name: "AdminkechengxinxiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengxinxi/updt.vue"),
        meta: { title: "编辑课程信息", authLogin: true },
    },
    {
        path: "kechengxinxi/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminkechengxinxiDetail",
        component: () => import("@/views/kechengxinxi/detail.vue"),
        meta: { title: "课程信息详情", authLogin: true },
    },
    {
        path: "kechengshipin",
        name: "AdminkechengshipinList",
        component: () => import("@/views/kechengshipin/list.vue"),
        meta: { title: "课程视频列表", authLogin: true },
    },

    {
        path: "kechengshipin/fabujiaoshi",
        name: "AdminkechengshipinListfabujiaoshi",
        component: () => import("@/views/kechengshipin/fabujiaoshi.vue"),
        meta: { title: "课程视频列表", authLogin: true },
    },

    {
        path: "kechengshipin/add",
        name: "AdminkechengshipinAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengshipin/add.vue"),
        meta: { title: "添加课程视频", authLogin: true },
    },
    {
        path: "kechengshipin/updt",
        name: "AdminkechengshipinUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengshipin/updt.vue"),
        meta: { title: "编辑课程视频", authLogin: true },
    },
    {
        path: "kechengshipin/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminkechengshipinDetail",
        component: () => import("@/views/kechengshipin/detail.vue"),
        meta: { title: "课程视频详情", authLogin: true },
    },
    {
        path: "kechengziyuan",
        name: "AdminkechengziyuanList",
        component: () => import("@/views/kechengziyuan/list.vue"),
        meta: { title: "课程资源列表", authLogin: true },
    },

    {
        path: "kechengziyuan/fabujiaoshi",
        name: "AdminkechengziyuanListfabujiaoshi",
        component: () => import("@/views/kechengziyuan/fabujiaoshi.vue"),
        meta: { title: "课程资源列表", authLogin: true },
    },

    {
        path: "kechengziyuan/add",
        name: "AdminkechengziyuanAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengziyuan/add.vue"),
        meta: { title: "添加课程资源", authLogin: true },
    },
    {
        path: "kechengziyuan/updt",
        name: "AdminkechengziyuanUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengziyuan/updt.vue"),
        meta: { title: "编辑课程资源", authLogin: true },
    },
    {
        path: "kechengziyuan/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminkechengziyuanDetail",
        component: () => import("@/views/kechengziyuan/detail.vue"),
        meta: { title: "课程资源详情", authLogin: true },
    },
    {
        path: "kechengxuexi",
        name: "AdminkechengxuexiList",
        component: () => import("@/views/kechengxuexi/list.vue"),
        meta: { title: "课程学习列表", authLogin: true },
    },

    {
        path: "kechengxuexi/fabujiaoshi",
        name: "AdminkechengxuexiListfabujiaoshi",
        component: () => import("@/views/kechengxuexi/fabujiaoshi.vue"),
        meta: { title: "课程学习列表", authLogin: true },
    },
    {
        path: "kechengxuexi/xueshengyonghu",
        name: "AdminkechengxuexiListxueshengyonghu",
        component: () => import("@/views/kechengxuexi/xueshengyonghu.vue"),
        meta: { title: "课程学习列表", authLogin: true },
    },

    {
        path: "kechengxuexi/add",
        name: "AdminkechengxuexiAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengxuexi/add.vue"),
        meta: { title: "添加课程学习", authLogin: true },
    },
    {
        path: "kechengxuexi/updt",
        name: "AdminkechengxuexiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/kechengxuexi/updt.vue"),
        meta: { title: "编辑课程学习", authLogin: true },
    },
    {
        path: "kechengxuexi/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminkechengxuexiDetail",
        component: () => import("@/views/kechengxuexi/detail.vue"),
        meta: { title: "课程学习详情", authLogin: true },
    },
    {
        path: "xuexijindu",
        name: "AdminxuexijinduList",
        component: () => import("@/views/xuexijindu/list.vue"),
        meta: { title: "学习进度列表", authLogin: true },
    },

    {
        path: "xuexijindu/fabujiaoshi",
        name: "AdminxuexijinduListfabujiaoshi",
        component: () => import("@/views/xuexijindu/fabujiaoshi.vue"),
        meta: { title: "学习进度列表", authLogin: true },
    },
    {
        path: "xuexijindu/xueshengyonghu",
        name: "AdminxuexijinduListxueshengyonghu",
        component: () => import("@/views/xuexijindu/xueshengyonghu.vue"),
        meta: { title: "学习进度列表", authLogin: true },
    },

    {
        path: "xuexijindu/add",
        name: "AdminxuexijinduAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xuexijindu/add.vue"),
        meta: { title: "添加学习进度", authLogin: true },
    },
    {
        path: "xuexijindu/updt",
        name: "AdminxuexijinduUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xuexijindu/updt.vue"),
        meta: { title: "编辑学习进度", authLogin: true },
    },
    {
        path: "xuexijindu/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminxuexijinduDetail",
        component: () => import("@/views/xuexijindu/detail.vue"),
        meta: { title: "学习进度详情", authLogin: true },
    },
    {
        path: "xuexijilu",
        name: "AdminxuexijiluList",
        component: () => import("@/views/xuexijilu/list.vue"),
        meta: { title: "学习记录列表", authLogin: true },
    },

    {
        path: "xuexijilu/fabujiaoshi",
        name: "AdminxuexijiluListfabujiaoshi",
        component: () => import("@/views/xuexijilu/fabujiaoshi.vue"),
        meta: { title: "学习记录列表", authLogin: true },
    },
    {
        path: "xuexijilu/xueshengyonghu",
        name: "AdminxuexijiluListxueshengyonghu",
        component: () => import("@/views/xuexijilu/xueshengyonghu.vue"),
        meta: { title: "学习记录列表", authLogin: true },
    },

    {
        path: "xuexijilu/add",
        name: "AdminxuexijiluAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xuexijilu/add.vue"),
        meta: { title: "添加学习记录", authLogin: true },
    },
    {
        path: "xuexijilu/updt",
        name: "AdminxuexijiluUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/xuexijilu/updt.vue"),
        meta: { title: "编辑学习记录", authLogin: true },
    },
    {
        path: "xuexijilu/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminxuexijiluDetail",
        component: () => import("@/views/xuexijilu/detail.vue"),
        meta: { title: "学习记录详情", authLogin: true },
    },
    {
        path: "buzhizuoye",
        name: "AdminbuzhizuoyeList",
        component: () => import("@/views/buzhizuoye/list.vue"),
        meta: { title: "布置作业列表", authLogin: true },
    },

    {
        path: "buzhizuoye/fabujiaoshi",
        name: "AdminbuzhizuoyeListfabujiaoshi",
        component: () => import("@/views/buzhizuoye/fabujiaoshi.vue"),
        meta: { title: "布置作业列表", authLogin: true },
    },

    {
        path: "buzhizuoye/add",
        name: "AdminbuzhizuoyeAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/buzhizuoye/add.vue"),
        meta: { title: "添加布置作业", authLogin: true },
    },
    {
        path: "buzhizuoye/updt",
        name: "AdminbuzhizuoyeUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/buzhizuoye/updt.vue"),
        meta: { title: "编辑布置作业", authLogin: true },
    },
    {
        path: "buzhizuoye/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminbuzhizuoyeDetail",
        component: () => import("@/views/buzhizuoye/detail.vue"),
        meta: { title: "布置作业详情", authLogin: true },
    },
    {
        path: "tijiaozuoye",
        name: "AdmintijiaozuoyeList",
        component: () => import("@/views/tijiaozuoye/list.vue"),
        meta: { title: "提交作业列表", authLogin: true },
    },

    {
        path: "tijiaozuoye/fabujiaoshi",
        name: "AdmintijiaozuoyeListfabujiaoshi",
        component: () => import("@/views/tijiaozuoye/fabujiaoshi.vue"),
        meta: { title: "提交作业列表", authLogin: true },
    },
    {
        path: "tijiaozuoye/tijiaoxuesheng",
        name: "AdmintijiaozuoyeListtijiaoxuesheng",
        component: () => import("@/views/tijiaozuoye/tijiaoxuesheng.vue"),
        meta: { title: "提交作业列表", authLogin: true },
    },

    {
        path: "tijiaozuoye/add",
        name: "AdmintijiaozuoyeAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/tijiaozuoye/add.vue"),
        meta: { title: "添加提交作业", authLogin: true },
    },
    {
        path: "tijiaozuoye/updt",
        name: "AdmintijiaozuoyeUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/tijiaozuoye/updt.vue"),
        meta: { title: "编辑提交作业", authLogin: true },
    },
    {
        path: "tijiaozuoye/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdmintijiaozuoyeDetail",
        component: () => import("@/views/tijiaozuoye/detail.vue"),
        meta: { title: "提交作业详情", authLogin: true },
    },
    {
        path: "zuoyepiyue",
        name: "AdminzuoyepiyueList",
        component: () => import("@/views/zuoyepiyue/list.vue"),
        meta: { title: "作业批阅列表", authLogin: true },
    },

    {
        path: "zuoyepiyue/fabujiaoshi",
        name: "AdminzuoyepiyueListfabujiaoshi",
        component: () => import("@/views/zuoyepiyue/fabujiaoshi.vue"),
        meta: { title: "作业批阅列表", authLogin: true },
    },
    {
        path: "zuoyepiyue/tijiaoxuesheng",
        name: "AdminzuoyepiyueListtijiaoxuesheng",
        component: () => import("@/views/zuoyepiyue/tijiaoxuesheng.vue"),
        meta: { title: "作业批阅列表", authLogin: true },
    },

    {
        path: "zuoyepiyue/add",
        name: "AdminzuoyepiyueAdd",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/zuoyepiyue/add.vue"),
        meta: { title: "添加作业批阅", authLogin: true },
    },
    {
        path: "zuoyepiyue/updt",
        name: "AdminzuoyepiyueUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/zuoyepiyue/updt.vue"),
        meta: { title: "编辑作业批阅", authLogin: true },
    },
    {
        path: "zuoyepiyue/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminzuoyepiyueDetail",
        component: () => import("@/views/zuoyepiyue/detail.vue"),
        meta: { title: "作业批阅详情", authLogin: true },
    },
    {
        path: "wenda",
        name: "AdminwendaList",
        component: () => import("@/views/wenda/list.vue"),
        meta: { title: "问答列表", authLogin: true },
    },

    {
        path: "wenda/add",
        name: "AdminwendaAdd",
        component: () => import("@/views/wenda/add.vue"),
        meta: { title: "添加问答", authLogin: true },
    },
    {
        path: "wenda/updt",
        name: "AdminwendaUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/wenda/updt.vue"),
        meta: { title: "编辑问答", authLogin: true },
    },
    {
        path: "wenda/detail",
        props: (route) => ({ id: route.query.id }),
        name: "AdminwendaDetail",
        component: () => import("@/views/wenda/detail.vue"),
        meta: { title: "问答详情", authLogin: true },
    },
    {
        path: "huida",
        name: "AdminhuidaList",
        component: () => import("@/views/huida/list.vue"),
        meta: { title: "回答列表", authLogin: true },
    },

    {
        path: "huida/add",
        name: "AdminhuidaAdd",
        component: () => import("@/views/huida/add.vue"),
        meta: { title: "添加回答", authLogin: true },
    },
    {
        path: "huida/updt",
        name: "AdminhuidaUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/huida/updt.vue"),
        meta: { title: "编辑回答", authLogin: true },
    },
    {
        path: "wendaxiaoxi",
        name: "AdminwendaxiaoxiList",
        component: () => import("@/views/wendaxiaoxi/list.vue"),
        meta: { title: "问答消息列表", authLogin: true },
    },

    {
        path: "wendaxiaoxi/add",
        name: "AdminwendaxiaoxiAdd",
        component: () => import("@/views/wendaxiaoxi/add.vue"),
        meta: { title: "添加问答消息", authLogin: true },
    },
    {
        path: "wendaxiaoxi/updt",
        name: "AdminwendaxiaoxiUpdt",
        props: (route) => ({ id: route.query.id }),
        component: () => import("@/views/wendaxiaoxi/updt.vue"),
        meta: { title: "编辑问答消息", authLogin: true },
    },
];
