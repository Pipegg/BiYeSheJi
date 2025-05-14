<template>
    <div class="zhu" :style="{ left: left + 'px', top: top + 'px' }" @mousedown="mousedown">
        <div v-if="dialogVisible" class="gpt-mask" @click="onMaskClick">
            <div class="gpt-center" @click.stop>
                <chatbot />
            </div>
        </div>
        <img :src="img" alt="智能问答" class="zhu-img" />
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import chatbot from './chatbot.vue';
import img from './img.png';

const DEFAULT_LEFT_OFFSET = 150; // 距离右边的默认距离
const DEFAULT_TOP_OFFSET = 150; // 距离底部的默认距离

const left = ref(window.innerWidth - DEFAULT_LEFT_OFFSET);
const top = ref(window.innerHeight - DEFAULT_TOP_OFFSET);
const dialogVisible = ref(false);
const isDragging = ref(false);
const startX = ref(0);
const startY = ref(0);
const startLeft = ref(0);
const startTop = ref(0);
const mouseDownTime = ref(0);
const hasMoved = ref(false);
const CLICK_THRESHOLD = 1000; // 点击判定时间阈值（毫秒）
const MOVE_THRESHOLD = 5; // 移动判定阈值（像素）
const isVisible = ref(true); // 是否显示小猪


// 从localStorage获取位置，如果没有则使用默认位置
onMounted(() => {
    // 清除之前保存的位置
    localStorage.removeItem('chatbotLeft');
    localStorage.removeItem('chatbotTop');
    
    // 设置新的默认位置
    left.value = window.innerWidth - DEFAULT_LEFT_OFFSET;
    top.value = window.innerHeight - DEFAULT_TOP_OFFSET;
    savePosition();
    
    // 监听窗口大小变化，确保小猪不会超出可视区域
    window.addEventListener('resize', handleResize);
});

// 处理窗口大小变化
const handleResize = () => {
    const maxLeft = window.innerWidth - 80; // 80px是小猪图片的宽度加上一些边距
    const maxTop = window.innerHeight - 80;
    
    if (left.value > maxLeft) {
        left.value = maxLeft;
    }
    if (top.value > maxTop) {
        top.value = maxTop;
    }
    
    savePosition();
};

// 保存位置到localStorage
const savePosition = () => {
    localStorage.setItem('chatbotLeft', left.value.toString());
    localStorage.setItem('chatbotTop', top.value.toString());
};

const mousedown = (e) => {
    // 如果点击的是图片
    if (e.target.classList.contains('zhu-img')) {
        mouseDownTime.value = Date.now();
        hasMoved.value = false;
        isDragging.value = true;
        startX.value = e.clientX;
        startY.value = e.clientY;
        startLeft.value = left.value;
        startTop.value = top.value;
        
        // 添加全局事件监听
        document.addEventListener('mousemove', mousemove);
        document.addEventListener('mouseup', mouseup);
    }
};

const mouseup = (e) => {
    if (e.target.classList.contains('zhu-img')) {
        const clickDuration = Date.now() - mouseDownTime.value;
        
        // 如果是快速点击且没有明显移动，则打开对话框
        if (clickDuration < CLICK_THRESHOLD && !hasMoved.value) {
            dialogVisible.value = true;
            isVisible.value = false;
        }
    }
    
    // 结束拖动
    isDragging.value = false;
    document.removeEventListener('mousemove', mousemove);
    document.removeEventListener('mouseup', mouseup);
    
    // 保存位置
    savePosition();
};

const mousemove = (e) => {
    if (!isDragging.value) return;
    
    const deltaX = e.clientX - startX.value;
    const deltaY = e.clientY - startY.value;
    
    // 检查是否移动超过阈值
    if (Math.abs(deltaX) > MOVE_THRESHOLD || Math.abs(deltaY) > MOVE_THRESHOLD) {
        hasMoved.value = true;
    }
    
    // 计算新位置（直接跟随鼠标位置）
    let newLeft = e.clientX - 30; // 30是图片宽度的一半，使鼠标位于图片中心
    let newTop = e.clientY - 30;  // 30是图片高度的一半，使鼠标位于图片中心
    
    // 限制不超出可视区域
    const maxLeft = window.innerWidth - 60; // 60是图片宽度
    const maxTop = window.innerHeight - 60; // 60是图片高度
    
    newLeft = Math.max(0, Math.min(newLeft, maxLeft));
    newTop = Math.max(0, Math.min(newTop, maxTop));
    
    left.value = newLeft;
    top.value = newTop;
};

onUnmounted(() => {
    document.removeEventListener('mousemove', mousemove);
    document.removeEventListener('mouseup', mouseup);
    window.removeEventListener('resize', handleResize);
});

const dialogWidth = computed(() => Math.floor(window.innerWidth * 2 / 3) + 'px');

const onMaskClick = () => {
    dialogVisible.value = false;
    isVisible.value = true;
};

const isImageMsg = (content) => {
    // 简单判断是否为图片链接
    return typeof content === 'string' && (
        content.match(/\.(jpeg|jpg|gif|png|webp)$/i) ||
        content.startsWith('http') && content.match(/(\/|=)[^\/=]+\.(jpeg|jpg|gif|png|webp)$/i)
    );
};
</script>

<style scoped lang="scss">
.zhu {
    position: fixed; // 固定定位
    z-index: 999; // 层级
    cursor: auto; // 鼠标样式
    
    .zhu-img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.3s; // 过渡效果
        
        &:hover {
            transform: scale(1.1); // 鼠标悬停时放大
        }
    }
}

:deep(.chat-dialog) {
    .el-dialog__header {
        padding: 15px 20px;
        margin: 0;
        border-bottom: 1px solid #e4e7ed;
    }
    .el-dialog__body {
        padding: 0;
    }
}

.gpt-mask {
    position: fixed;
    z-index: 2000;
    left: 0; top: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: auto;
}
.gpt-center {
    display: flex;
    justify-content: center;
    align-items: center;
    transform: translate(400px, 100px);
}

.gpt-chat-root {
    width: 600px;
    height: 60vh;
    max-height: 80vh;
    margin: auto;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.10);
    display: flex;
    flex-direction: column;
    position: relative;
    box-sizing: border-box;
    word-break: break-all;
    overflow: hidden;
}

.gpt-msg-row {
    display: flex;
    align-items: flex-end;
    gap: 12px;
    width: 100%;
    margin-bottom: 8px;
}
.ai-row {
    flex-direction: row;
    justify-content: flex-start;
}
.user-row {
    flex-direction: row-reverse;
    justify-content: flex-end;
}
.gpt-msg-avatar {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: #fff;
    border: 1px solid #eee;
}
.gpt-msg-bubble {
    max-width: 70%;
    padding: 12px 16px;
    font-size: 15px;
    line-height: 1.7;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    word-break: break-word;
    white-space: pre-line;
    display: flex;
    align-items: center;
}
.ai-bubble {
    background: #f7f7f8;
    color: #222;
    border-top-left-radius: 4px;
}
.user-bubble {
    background: #96EB6A;
    color: #222;
    border-top-right-radius: 4px;
}
.gpt-msg-img {
    max-width: 120px;
    max-height: 120px;
    border-radius: 8px;
    display: block;
    margin: 0 auto;
}

@media screen and (min-width: 1300px) {
  .e-container {
    width: 1000px; // 或 900px
  }
}
</style>