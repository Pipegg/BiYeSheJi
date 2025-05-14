/**
 * 服务器后端地址 格式为：http://{IP地址}:{端口号}
 * @type {string}
 */
let service_url = import.meta.env.VITE_API_URL || "http://127.0.0.1:8006";

// 开发环境下使用的地址
if (import.meta.env.DEV) {
    service_url = "http://127.0.0.1:8006";
}

/**
 * 系统配置信息
 */
const config = {
    service_url,
    title: "基于大模型的智能教育辅助系统的设计与实现",
    /**
     * 登录地址
     */
    login_url: "/login/?a=a",
    /**
     * token获取用户信息地址
     */
    token_login: "/tokenLogin/",
    /**
     * 退出登录地址
     */
    logout_login: "/logout/",
    /**
     * 查询数据
     */
    query_url: "/query/",
    /**
     * 查询数据
     */
    select_url: "/select/",

    uploadUrl: "/upload/",

    /**
     * 修改密码地址
     */
    user_mod_post: "/mod/",

    captch_url: "/captch/",
    
    /**
     * AI服务配置
     */
    ai_service: {
        enabled: false, // 暂时禁用AI服务
        base_url: "http://127.0.0.1:8006/ai",  // 改用本地代理
        model_settings: "/model_settings",
        extensions: "/extensions"
    }
};

export default config;
