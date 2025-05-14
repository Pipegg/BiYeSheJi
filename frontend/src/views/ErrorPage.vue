<template>
  <div class="error-page">
    <el-result
      icon="warning"
      title="页面加载错误"
      sub-title="抱歉，请求的页面无法加载，请稍后再试。"
    >
      <template #extra>
        <el-button type="primary" @click="goHome">返回首页</el-button>
        <el-button @click="retry">重试</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const retry = () => {
  window.location.reload()
}
</script>

<style scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 20px;
}
</style> 