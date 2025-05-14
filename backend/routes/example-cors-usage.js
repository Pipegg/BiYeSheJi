/**
 * 示例：如何在Express.js中使用CORS配置
 * 此文件展示了如何在后端API路由中正确配置CORS
 */

const express = require('express');
const cors = require('cors');
const { corsOptions, learningApiCorsOptions } = require('./cors-config');

// 创建路由器
const router = express.Router();

// 默认CORS中间件
const defaultCors = cors(corsOptions);

// 特殊API的CORS中间件
const learningApiCors = cors(learningApiCorsOptions);

// 学习分析API路由示例
// 对所有 /api/ai/learning-analysis 的请求使用宽松的CORS设置
router.use('/api/ai/learning-analysis', learningApiCors);
router.use('/api/ai/analysis', learningApiCors);

// 学习分析列表API
router.get('/api/ai/learning-analysis/list', async (req, res) => {
  try {
    // 设置明确的CORS标头（备用）
    res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
    res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, token');
    res.header('Access-Control-Allow-Credentials', 'true');
    
    // 模拟API响应
    const mockData = {
      code: 0,
      msg: '获取学习分析列表成功',
      data: {
        overall_progress: 75,
        strengths: ['编程基础', '数据结构', '系统设计'],
        weaknesses: ['数据库优化', '高级算法'],
        suggestions: [
          '建议加强数据库性能优化的学习',
          '可以通过实践项目来提升高级算法应用能力',
          '继续保持编程基础的学习和巩固'
        ]
      }
    };
    
    // 延迟响应以模拟网络延迟
    setTimeout(() => {
      res.json(mockData);
    }, 300);
  } catch (error) {
    console.error('学习分析列表API错误:', error);
    res.status(500).json({
      code: 500,
      msg: '服务器内部错误',
      error: error.message
    });
  }
});

// 简单学习分析API
router.get('/api/ai/learning-analysis', async (req, res) => {
  // 重用与列表API相同的逻辑
  try {
    res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
    res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, token');
    res.header('Access-Control-Allow-Credentials', 'true');
    
    const mockData = {
      code: 0,
      msg: '获取学习分析成功',
      data: {
        overall_progress: 75,
        strengths: ['编程基础', '数据结构', '系统设计'],
        weaknesses: ['数据库优化', '高级算法'],
        suggestions: [
          '建议加强数据库性能优化的学习',
          '可以通过实践项目来提升高级算法应用能力',
          '继续保持编程基础的学习和巩固'
        ]
      }
    };
    
    setTimeout(() => {
      res.json(mockData);
    }, 300);
  } catch (error) {
    console.error('学习分析API错误:', error);
    res.status(500).json({
      code: 500,
      msg: '服务器内部错误',
      error: error.message
    });
  }
});

// AI分析API (另一个端点)
router.get('/api/ai/analysis', async (req, res) => {
  try {
    res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
    res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, token');
    res.header('Access-Control-Allow-Credentials', 'true');
    
    const mockData = {
      code: 0,
      msg: '获取AI分析成功',
      data: {
        overall_progress: 75,
        strengths: ['编程基础', '数据结构', '系统设计'],
        weaknesses: ['数据库优化', '高级算法'],
        suggestions: [
          '建议加强数据库性能优化的学习',
          '可以通过实践项目来提升高级算法应用能力',
          '继续保持编程基础的学习和巩固'
        ]
      }
    };
    
    setTimeout(() => {
      res.json(mockData);
    }, 300);
  } catch (error) {
    console.error('AI分析API错误:', error);
    res.status(500).json({
      code: 500,
      msg: '服务器内部错误',
      error: error.message
    });
  }
});

// 对预检请求的特殊处理
// 这是为了解决某些浏览器可能发送的预检请求问题
router.options('/api/ai/learning-analysis*', learningApiCors, (req, res) => {
  // 预检请求处理
  res.header('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, token, user-agent, accept, origin, referer, accept-encoding, accept-language, content-length');
  res.header('Access-Control-Allow-Credentials', 'true');
  res.status(204).end();
});

// 导出路由器
module.exports = router;

/**
 * 在主应用文件中使用该路由的示例:
 * 
 * const express = require('express');
 * const app = express();
 * const apiRoutes = require('./routes/example-cors-usage');
 * 
 * // 使用API路由
 * app.use('/', apiRoutes);
 * 
 * // 启动服务器
 * const port = process.env.PORT || 8006;
 * app.listen(port, () => {
 *   console.log(`服务器运行在 http://localhost:${port}`);
 * });
 */ 