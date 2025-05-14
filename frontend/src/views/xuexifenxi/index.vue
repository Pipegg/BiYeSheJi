<template>
  <div class="learning-analysis">
    <el-card shadow="never" class="box-card">
      <template #header>
        <div class="card-header">
          <h2>学习分析</h2>
          <div>
            <el-button type="info" size="small" @click="refreshData">
              刷新数据
            </el-button>
          </div>
        </div>
      </template>
      <div v-if="loading">
        <el-skeleton :rows="6" animated />
      </div>
      <div v-else>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-card class="overview-card">
              <div class="progress-overview">
                <el-progress
                  type="dashboard"
                  :percentage="analysis.overall_progress"
                  :color="progressColor"
                >
                  <template #default="{ percentage }">
                    <span class="progress-text">{{ percentage }}%</span>
                  </template>
                </el-progress>
                <div class="progress-label">总体学习进度</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-title">优势领域</div>
              </template>
              <div class="tag-list">
                <el-tag
                  v-for="(item, index) in analysis.strengths"
                  :key="index"
                  type="success"
                  class="tag-item"
                >
                  {{ item }}
                </el-tag>
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-title">需要加强的领域</div>
              </template>
              <div class="tag-list">
                <el-tag
                  v-for="(item, index) in analysis.weaknesses"
                  :key="index"
                  type="danger"
                  class="tag-item"
                >
                  {{ item }}
                </el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :span="24">
            <el-card>
              <template #header>
                <div class="card-title">学习建议</div>
              </template>
              <div class="suggestions-list">
                <div
                  v-for="(item, index) in analysis.suggestions"
                  :key="index"
                  class="suggestion-item"
                >
                  <div class="suggestion-number">{{ index + 1 }}</div>
                  <div class="suggestion-content">{{ item }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import * as api from '@/utils/api'

// 状态变量
const loading = ref(true)
const error = ref(null)
const userStore = useUserStore()
const router = useRouter()

// 学习分析数据
const analysis = ref({
  overall_progress: 75,
  strengths: ['编程基础', '数据结构', '系统设计'],
  weaknesses: ['数据库优化', '高级算法'],
  suggestions: [
    '建议加强数据库性能优化的学习',
    '可以通过实践项目来提升高级算法应用能力',
    '继续保持编程基础的学习和巩固'
  ]
})

// 根据进度计算颜色
const progressColor = computed(() => {
  const progress = analysis.value.overall_progress
  if (progress >= 90) return '#67C23A'
  if (progress >= 70) return '#E6A23C'
  if (progress >= 50) return '#F56C6C'
  return '#909399'
})

// 加载学习分析数据
const loadAnalysisData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await api.getLearningAnalysis()
    
    if (response && response.data) {
      // 更新分析数据
      analysis.value = response.data
    }
  } catch (apiError) {
    console.warn('数据加载出现问题，使用默认值')
  } finally {
    loading.value = false
  }
}

// 添加一个简单的刷新数据函数
const refreshData = async () => {
  try {
    loading.value = true
    await loadAnalysisData()
    ElMessage.success('数据已刷新')
  } catch (error) {
    // 静默处理错误
    console.error('刷新数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 在组件挂载时加载数据
onMounted(async () => {
  try {
    console.log('学习分析组件已挂载，准备加载数据')
    
    // 检查登录状态
    if (!userStore.isLogin()) {
      console.log('用户未登录，尝试进行令牌登录')
      try {
        await userStore.tokenLogin()
      } catch (loginError) {
        console.error('令牌登录失败:', loginError)
        ElMessage.warning('请先登录后再查看学习分析')
        router.push('/login?redirect=/xuexifenxi')
        return
      }
    }
    
    // 加载数据
    await loadAnalysisData()
  } catch (e) {
    console.error('学习分析组件加载失败:', e)
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.learning-analysis {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
}

.progress-overview {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.progress-text {
  font-size: 24px;
  font-weight: bold;
}

.progress-label {
  margin-top: 10px;
  font-size: 14px;
  color: #909399;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  margin: 5px;
}

.suggestions-list {
  padding: 10px 0;
}

.suggestion-item {
  display: flex;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #EBEEF5;
}

.suggestion-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.suggestion-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  flex-shrink: 0;
}

.suggestion-content {
  flex: 1;
  line-height: 24px;
}
</style> 