<template>
  <div class="learning-path-container">
    <el-card v-if="isLoading">
      <div style="display: flex; justify-content: center; align-items: center; height: 300px;" v-loading="true">
        <span>加载中...</span>
      </div>
    </el-card>
    <el-card v-else-if="authError">
      <div style="text-align: center; padding: 40px;">
        <h3>需要登录</h3>
        <p>请先登录，然后再访问学习路径</p>
        <el-button type="primary" @click="redirectToLogin">去登录</el-button>
      </div>
    </el-card>
    <el-card v-else>
      <div class="header">
        <h2>你的专属学习路径</h2>
        <el-button type="primary" @click="regeneratePath" :loading="regenerating">再生成路径</el-button>
      </div>
      <el-steps :active="activeStep" finish-status="success" align-center>
        <el-step
          v-for="(step, index) in path"
          :key="step.id"
          :title="step.title"
          :description="step.description"
          :status="step.completed ? 'success' : (index === activeStep ? 'process' : 'wait')">
          <template #description>
            <div>
              <span>{{ step.description }}</span>
              <el-button
                v-if="!step.completed && index === activeStep"
                size="mini"
                type="success"
                @click="markCompleted(step, index)"
                :loading="marking"
                style="margin-left: 10px;">进度打卡</el-button>
            </div>
          </template>
        </el-step>
      </el-steps>
      <el-timeline style="margin-top: 40px;">
        <el-timeline-item
          v-for="(step, index) in path"
          :key="step.id"
          :timestamp="step.timestamp"
          :color="step.completed ? '#67C23A' : '#909399'">
          {{ step.title }}
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from 'axios';
import { useUserStore } from "@/stores";
import { useRouter } from 'vue-router';
import { aiHttp } from "@/utils/ajax/http";

const path = ref([]);
const activeStep = ref(0);
const marking = ref(false);
const regenerating = ref(false);
const pathId = ref(null);
const isLoading = ref(true);
const authError = ref(false);
const router = useRouter();
const userStore = useUserStore();

const redirectToLogin = () => {
  ElMessageBox.confirm("您需要先登录才能访问学习路径，是否前往登录？", "需要登录", {
    confirmButtonText: "去登录",
    cancelButtonText: "取消",
    type: "warning"
  }).then(() => {
    // 触发全局登录事件，让顶部栏显示登录框
    window.dispatchEvent(new CustomEvent('show-login-form'));
    
    // 如果在3秒内没有触发登录框，回退到首页
    setTimeout(() => {
      router.push('/');
    }, 3000);
  }).catch(() => {
    router.push('/');
  });
};

const fetchPath = async (retryCount = 0) => {
  isLoading.value = true;
  authError.value = false;
  
  // Check if user is logged in
  if (!userStore.isLogin()) {
    console.log('User not logged in, attempting token login');
    try {
      // Try to recover login state from token
      await userStore.tokenLogin();
      // Check if login was successful
      if (!userStore.isLogin()) {
        console.log('Token login failed, redirecting to login');
        authError.value = true;
        isLoading.value = false;
        return;
      }
    } catch (error) {
      console.error('Token login failed with error:', error);
      authError.value = true;
      isLoading.value = false;
      return;
    }
  }
  
  try {
    console.log('Fetching learning path with token:', userStore.token ? userStore.token.substring(0, 15) + '...' : 'null');
    console.log('Session信息:', userStore.session);
    
    // 准备请求数据
    const url = '/api/ai/learning-path/';
    const requestData = {
      token: userStore.token,
      _t: Date.now() // 时间戳防止缓存
    };
    
    // 添加完整的用户认证信息
    if (userStore.session) {
      if (userStore.session.username) {
        requestData.username = userStore.session.username;
      }
      
      if (userStore.session.id) {
        requestData.user_id = userStore.session.id;
      }
      
      // 添加表名信息
      if (userStore.session.table) {
        requestData.table = userStore.session.table;
      } else if (userStore.session.cx === '学生') {
        requestData.table = 'xuesheng';
      } else if (userStore.session.cx === '教师') {
        requestData.table = 'jiaoshi';
      }
      
      // 添加其他可能有用的信息
      if (userStore.session.cx) {
        requestData.cx = userStore.session.cx;
      }
    }
    
    // 添加角色信息
    if (userStore.roles) {
      requestData.roles = userStore.roles;
    }
    
    console.log('学习路径请求数据:', requestData);
    
    // 请求配置 - 增强认证
    const requestConfig = {
      headers: {
        'token': userStore.token,
        'Authorization': `Bearer ${userStore.token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      withCredentials: true // 尝试添加cookie支持
    };
    
    let res;
    try {
      // 使用POST方法代替GET，将参数放在请求体而不是URL中
      res = await aiHttp.post(`${url}fetch/`, requestData, requestConfig);
      console.log('学习路径API响应:', res);
    } catch (error) {
      console.error('学习路径请求失败:', error);
      
      // 检查是否为认证错误
      if (error.authError || (error.response && (error.response.status === 401 || error.response.status === 403))) {
        console.warn('认证失败，无法访问学习路径');
        
        // 如果尚未达到最大重试次数且有token，则尝试重试
        if (retryCount < 3 && userStore.token) {
          console.log(`尝试第${retryCount + 1}次重试获取学习路径...`);
          
          // 在重试前尝试刷新token
          try {
            console.log('尝试刷新token...');
            await userStore.tokenLogin();
            console.log('Token刷新完成，使用新token重试');
            
            // 检查token刷新后的登录状态
            if (!userStore.isLogin() && retryCount >= 1) {
              console.warn('多次尝试后仍未能恢复登录状态');
              authError.value = true;
              isLoading.value = false;
              return;
            }
          } catch (tokenError) {
            console.error('Token刷新失败:', tokenError);
            
            // 如果是最后一次尝试，则放弃
            if (retryCount >= 2) {
              authError.value = true;
              isLoading.value = false;
              return;
            }
          }
          
          // 短暂延迟后重试
          setTimeout(() => {
            fetchPath(retryCount + 1);
          }, 1000);
          return;
        }
        
        authError.value = true;
        isLoading.value = false;
        return;
      }
      
      // 如果返回404（没有学习路径），尝试创建一个
      if (error.response && error.response.status === 404) {
        console.log('No learning path found, creating a default one');
        // 使用aiHttp创建新的学习路径
        const createData = {
          subject: '计算机科学',
          level: '初级',
          token: userStore.token
        };
        
        // 添加用户信息
        if (userStore.session) {
          createData.username = userStore.session.username || '';
          createData.user_id = userStore.session.id || '';
          
          // 添加表名
          if (userStore.session.table) {
            createData.table = userStore.session.table;
          } else if (userStore.session.cx === '学生') {
            createData.table = 'xuesheng';
          } else if (userStore.session.cx === '教师') {
            createData.table = 'jiaoshi';
          }
        }
        
        console.log('创建学习路径数据:', createData);
        res = await aiHttp.post('/api/ai/learning-path/', createData, requestConfig);
        console.log('创建学习路径响应:', res);
      } else {
        // 重新抛出其他错误
        throw error;
      }
    }
    
    // 处理响应数据
    let pathData = res;
    
    // 从不同的响应结构中提取数据
    if (res && res.data) {
      // axios响应
      pathData = res.data;
    }
    
    // 调试输出响应数据结构
    console.log('学习路径数据结构:', JSON.stringify(pathData).substring(0, 200) + '...');
    
    // 处理不同格式的学习路径数据
    if (Array.isArray(pathData) && pathData.length > 0) {
      pathId.value = pathData[0].id;
      // 假设order为阶段顺序，progress为完成情况
      path.value = pathData[0].order.map((title, idx) => ({
        id: idx,
        title,
        description: pathData[0].content[idx] || '',
        completed: pathData[0].progress[idx] === 1,
        timestamp: '' // 可根据需要补充
      }));
      activeStep.value = path.value.findIndex(step => !step.completed);
      if (activeStep.value === -1) activeStep.value = path.value.length;
    } else if (typeof pathData === 'object' && pathData.order) {
      // 单个对象的情况
      pathId.value = pathData.id;
      path.value = pathData.order.map((title, idx) => ({
        id: idx,
        title,
        description: pathData.content[idx] || '',
        completed: pathData.progress[idx] === 1,
        timestamp: ''
      }));
      activeStep.value = path.value.findIndex(step => !step.completed);
      if (activeStep.value === -1) activeStep.value = path.value.length;
    } else {
      console.warn('无法解析学习路径数据:', pathData);
      path.value = [];
      pathId.value = null;
    }
  } catch (e) {
    console.error('获取学习路径失败:', e);
    if (e.response && (e.response.status === 401 || e.response.status === 403)) {
      authError.value = true;
      ElMessage.error('认证失败，请重新登录后再访问学习路径');
    } else {
      ElMessage.error('获取学习路径失败：' + (e.message || '未知错误'));
    }
  } finally {
    isLoading.value = false;
  }
};

const markCompleted = async (step, index) => {
  if (pathId.value === null) return;
  marking.value = true;
  try {
    // 准备请求配置
    const endpoint = `/api/ai/learning-path/${pathId.value}/mark_stage/`;
    const data = { 
      stage_index: index, 
      status: 1,
      token: userStore.token
    };
    
    console.log('发送进度打卡请求:', endpoint);
    
    // 使用简化的请求方式
    const requestConfig = {
      headers: {
        'token': userStore.token,
        'Authorization': `Bearer ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    };
    
    const res = await aiHttp.post(endpoint, data, requestConfig);
    
    ElMessage.success('进度打卡成功');
    await fetchPath();
  } catch (e) {
    console.error('打卡失败:', e);
    if (e.authError || (e.response && (e.response.status === 401 || e.response.status === 403))) {
      authError.value = true;
      ElMessage.error('认证失败，请重新登录');
    } else {
      ElMessage.error('打卡失败: ' + (e.message || '未知错误'));
    }
  } finally {
    marking.value = false;
  }
};

const regeneratePath = async () => {
  if (pathId.value === null) return;
  regenerating.value = true;
  try {
    // 准备请求配置
    const endpoint = `/api/ai/learning-path/${pathId.value}/regenerate/`;
    const data = { 
      token: userStore.token
    };
    
    console.log('发送重新生成请求:', endpoint);
    
    // 使用简化的请求方式
    const requestConfig = {
      headers: {
        'token': userStore.token,
        'Authorization': `Bearer ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    };
    
    const res = await aiHttp.post(endpoint, data, requestConfig);
    
    ElMessage.success('学习路径已重新生成');
    await fetchPath();
  } catch (e) {
    console.error('再生成失败:', e);
    if (e.authError || (e.response && (e.response.status === 401 || e.response.status === 403))) {
      authError.value = true;
      ElMessage.error('认证失败，请重新登录');
    } else {
      ElMessage.error('再生成失败: ' + (e.message || '未知错误'));
    }
  } finally {
    regenerating.value = false;
  }
};

onMounted(fetchPath);
</script>

<style scoped>
.learning-path-container {
  max-width: 900px;
  margin: 40px auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 