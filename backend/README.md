# 学习分析 API 服务器

这是一个简单的 Express.js 服务器，提供学习分析相关的 API 端点，供前端应用调用。

## 功能

- 提供学习分析数据的 API 端点
- 支持 CORS 跨域请求
- 包含基本的 JWT 令牌验证

## API 端点

- `/api/ai/learning-analysis/list` - 获取学习分析列表
- `/api/ai/learning-analysis` - 获取学习分析数据
- `/api/ai/analysis` - 获取 AI 分析数据

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动服务器

```bash
npm start
```

或者在 Windows 上，您可以直接双击 `start.bat` 文件。

服务器将在 http://localhost:8006 上运行。

## 开发模式

使用 nodemon 实时重载：

```bash
npm run dev
```

## 技术栈

- Express.js - Web 框架
- cors - 处理跨域资源共享
- jsonwebtoken - JWT 令牌验证
- body-parser - 请求体解析 