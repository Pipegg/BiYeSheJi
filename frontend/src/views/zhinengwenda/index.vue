<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>智能问答</h2>
      <el-button type="danger" size="small" @click="clearHistory">清空对话历史</el-button>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
        <div class="message-content" v-html="formatMessage(message.content)"></div>
        <div class="message-time">{{ formatTime(message.timestamp) }}</div>
      </div>
      
      <div v-if="loading" class="message assistant-message">
        <div class="message-content">
          <el-icon class="is-loading"><Loading /></el-icon>
          正在思考...
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <el-input
        v-model="question"
        type="textarea"
        :rows="3"
        placeholder="请输入你的问题，按Enter发送，Shift+Enter换行"
        @keydown.enter.prevent="handleEnter"
      />
      <el-button type="primary" :loading="loading" @click="sendQuestion">
        发送
      </el-button>
    </div>
    
    <div v-if="followUpQuestions.length > 0" class="follow-up-questions">
      <h4>相关问题：</h4>
      <el-tag
        v-for="(q, index) in followUpQuestions"
        :key="index"
        class="follow-up-tag"
        @click="selectFollowUpQuestion(q)"
      >
        {{ q }}
      </el-tag>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { authGet, authPost } from '@/utils/api'
import { marked } from 'marked'

const userStore = useUserStore()
const router = useRouter()
const messagesContainer = ref(null)
const question = ref('')
const loading = ref(false)
const messages = ref([])
const followUpQuestions = ref([])

// 检查用户是否已登录
const checkLogin = () => {
  if (!userStore.isLogin()) {
    ElMessage.warning('请先登录后再使用智能问答')
    // 指定前端登录页面，避免跳转到管理员登录
    router.push('/login?redirect=/zhinengwenda')
    return false
  }
  return true
}

// 获取用户ID，支持多种属性名
const getUserId = () => {
  if (userStore.userId) return userStore.userId
  if (userStore.session && userStore.session.username) return userStore.session.username
  return ''
}

// 加载历史消息
const loadHistory = async () => {
  if (!checkLogin()) return
  
  try {
    // 添加调试输出
    console.log('开始加载历史消息，当前用户状态:', {
      isLogin: userStore.isLogin(),
      hasToken: !!userStore.token,
      userId: getUserId(),
      extraParams: {
        role: 'student',
        redirect_url: '/zhinengwenda'
      }
    })
    
    // 添加用户角色信息，使用直接URL
    const response = await authGet('/api/chat/history/', {
      params: {
        role: 'student',
        redirect_url: '/zhinengwenda'
      },
      useDirectUrl: true // 启用直接URL模式
    })
    
    console.log('历史消息加载响应:', response)
    
    messages.value = response.data
    scrollToBottom()
  } catch (error) {
    console.error('加载历史消息失败:', error)
    
    // 检查错误响应详情
    console.log('错误详情:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      message: error.message
    })
    
    // 打印原始错误响应内容
    try {
      console.log('原始错误响应:', {
        responseData: JSON.stringify(error.response?.data),
        responseHeaders: Object.fromEntries(
          Object.entries(error.response?.headers || {})
        ),
        responseType: error.response?.headers?.['content-type']
      });
    } catch (e) {
      console.log('无法解析错误响应数据:', e);
    }
    
    // 尝试直接访问后端API
    try {
      console.log('尝试直接访问后端API获取历史消息');
      
      const axios = (await import('axios')).default;
      const token = userStore.token;
      const userId = getUserId();
      
      const directResponse = await axios({
        url: 'http://127.0.0.1:8006/api/chat/history/',
        method: 'get',
        headers: {
          'Authorization': `Bearer ${token}`,
          'token': token,
          'Content-Type': 'application/json'
        },
        params: {
          role: 'student',
          user_id: userId,
          token: token,
          redirect_url: '/zhinengwenda',
          timestamp: Date.now()
        },
        withCredentials: true
      });
      
      console.log('直接请求响应:', directResponse.data);
      
      if (directResponse.data) {
        messages.value = directResponse.data.data || directResponse.data;
        scrollToBottom();
        ElMessage.success('历史消息加载成功(直接访问)');
      }
    } catch (directError) {
      console.error('直接请求失败:', directError);
      
      // 检查错误响应是否包含关于后台登录的信息
      const errorMsg = error.response?.data?.msg || '';
      if (errorMsg.includes('后台') || errorMsg.includes('admin')) {
        ElMessage.warning('系统错误：不应该跳转到后台登录。正在修正...')
        setTimeout(() => {
          // 强制跳转到前端登录
          router.push('/login?redirect=/zhinengwenda')
        }, 1000)
      } else {
        ElMessage.error('加载历史消息失败，请稍后重试')
      }
    }
  }
}

// 发送问题
const sendQuestion = async () => {
  if (!checkLogin()) return
  if (!question.value.trim()) return
  
  const userMessage = {
    role: 'user',
    content: question.value,
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  loading.value = true
  followUpQuestions.value = []
  
  try {
    // 添加调试输出
    console.log('发送问题:', {
      question: question.value,
      userId: getUserId(),
      role: 'student'
    })
    
    // 使用直接URL模式
    const response = await authPost('/api/chat/ask/', {
      question: question.value,
      role: 'student'  // 明确指定角色
    }, {
      useDirectUrl: true // 启用直接URL模式
    })
    
    console.log('问题回答响应:', response)
    
    const assistantMessage = {
      role: 'assistant',
      content: response.data.answer,
      timestamp: new Date().toISOString()
    }
    
    messages.value.push(assistantMessage)
    
    // 获取后续问题建议，使用直接URL
    const followUpResponse = await authPost('/api/chat/follow-up/', {
      question: question.value,
      answer: response.data.answer,
      role: 'student'  // 明确指定角色
    }, {
      useDirectUrl: true // 启用直接URL模式
    })
    
    console.log('后续问题建议响应:', followUpResponse)
    
    followUpQuestions.value = followUpResponse.data.questions
    
  } catch (error) {
    console.error('发送消息失败:', error)
    
    // 检查错误响应详情
    console.log('错误详情:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      message: error.message
    })
    
    // 打印原始错误响应内容
    try {
      console.log('原始错误响应:', {
        responseData: JSON.stringify(error.response?.data),
        responseHeaders: Object.fromEntries(
          Object.entries(error.response?.headers || {})
        ),
        responseType: error.response?.headers?.['content-type']
      });
    } catch (e) {
      console.log('无法解析错误响应数据:', e);
    }
    
    ElMessage.error('发送消息失败')
  } finally {
    loading.value = false
    question.value = ''
    scrollToBottom()
  }
}

// 清空历史
const clearHistory = async () => {
  if (!checkLogin()) return
  
  try {
    await authPost('/api/chat/clear/')
    messages.value = []
    followUpQuestions.value = []
    ElMessage.success('对话历史已清空')
  } catch (error) {
    console.error('清空历史失败:', error)
    ElMessage.error('清空历史失败')
  }
}

// 选择后续问题
const selectFollowUpQuestion = (q) => {
  question.value = q
  sendQuestion()
}

// 处理Enter键
const handleEnter = (e) => {
  if (e.shiftKey) return
  sendQuestion()
}

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
  try {
    if (!content) return '';
    return marked(content);
  } catch (error) {
    console.error('Markdown 渲染错误:', error);
    return content || '';
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  loadHistory()
})
</script>

<style lang="scss" scoped>
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
  
  .chat-header {
    padding: 16px;
    background: #fff;
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
      font-size: 18px;
      color: #303133;
    }
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    
    .message {
      margin-bottom: 16px;
      max-width: 80%;
      
      .message-content {
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.6;
        
        :deep(pre) {
          background: #f8f9fa;
          padding: 12px;
          border-radius: 4px;
          overflow-x: auto;
        }
        
        :deep(code) {
          background: #f8f9fa;
          padding: 2px 4px;
          border-radius: 4px;
        }
      }
      
      .message-time {
        font-size: 12px;
        color: #909399;
        margin-top: 4px;
      }
    }
    
    .user-message {
      margin-left: auto;
      
      .message-content {
        background: #409eff;
        color: #fff;
      }
      
      .message-time {
        text-align: right;
      }
    }
    
    .assistant-message {
      margin-right: auto;
      
      .message-content {
        background: #fff;
        color: #303133;
      }
    }
  }
  
  .chat-input {
    padding: 16px;
    background: #fff;
    border-top: 1px solid #e4e7ed;
    display: flex;
    gap: 12px;
    
    .el-textarea {
      flex: 1;
    }
  }
  
  .follow-up-questions {
    padding: 12px 16px;
    background: #fff;
    border-top: 1px solid #e4e7ed;
    
    h4 {
      margin: 0 0 8px;
      font-size: 14px;
      color: #606266;
    }
    
    .follow-up-tag {
      margin-right: 8px;
      margin-bottom: 8px;
      cursor: pointer;
      
      &:hover {
        opacity: 0.8;
      }
    }
  }
}
</style> 