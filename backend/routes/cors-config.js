/**
 * CORS 配置
 * 允许前端应用进行跨域请求，特别是学习分析相关API
 */

const corsOptions = {
  // 允许的来源，可以是具体域名或通配符
  origin: function (origin, callback) {
    // 允许的来源列表
    const allowedOrigins = [
      // 开发环境
      'http://localhost:5173',
      'http://localhost:5174',
      'http://127.0.0.1:5173',
      'http://127.0.0.1:5174',
      // 生产环境
      'https://your-production-domain.com'
    ];
    
    // null 表示同源请求（如 curl、postman 等）
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      console.warn(`CORS: 拒绝来自 ${origin} 的请求`);
      callback(new Error(`不允许来自 ${origin} 的CORS请求`));
    }
  },
  
  // 允许的请求方法
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  
  // 允许的请求头
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-Requested-With',
    'token'
  ],
  
  // 允许暴露的响应头
  exposedHeaders: ['Content-Length', 'X-Rate-Limit'],
  
  // 允许携带凭证（如 cookies）
  credentials: true,
  
  // 预检请求缓存时间，单位秒
  maxAge: 86400, // 24小时
  
  // 允许请求头中包含的字段
  preflightContinue: false,
  
  // 记录CORS错误
  optionsSuccessStatus: 204
};

// 特殊API的CORS设置
const learningApiCorsOptions = {
  ...corsOptions,
  // 允许所有来源
  origin: true,
  // 为学习分析API放宽限制，允许更多请求头
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-Requested-With',
    'token',
    'user-agent',
    'accept',
    'origin',
    'referer',
    'accept-encoding',
    'accept-language',
    'content-length'
  ]
};

module.exports = {
  corsOptions,
  learningApiCorsOptions
}; 