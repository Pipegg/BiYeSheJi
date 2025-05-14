<template>
    <el-button @click="check" v-if="$session.username" v-bind="$attrs">
        <slot>聊天 </slot>
    </el-button>
</template>
<style lang="scss">

</style>
<script>
import {useChatStore} from "@/stores/chat";

export default {
    name: "e-chat-check",
    data() {
        return {
            isProcessing: false
        }
    },
    props:{
        rid:{
            type:[String,Number],
            required: true
        },
    },
    methods: {
        check(){
            if (this.isProcessing) {
                console.log('已经在处理中，请等待');
                return;
            }
            
            this.isProcessing = true;
            console.log('启动聊天对话，教师ID:', this.rid, '学生ID:', this.$session.username);
            
            try {
                const obj = {
                    rid: this.rid,
                    sid: this.$session.username
                };
                
                // 调用聊天store的check方法创建/获取聊天会话
                useChatStore().check(obj)
                    .then(() => {
                        console.log('聊天对话创建成功');
                        this.isProcessing = false;
                    })
                    .catch(error => {
                        console.error('聊天对话创建失败:', error);
                        this.isProcessing = false;
                    });
            } catch (error) {
                console.error('聊天对话处理异常:', error);
                this.isProcessing = false;
            }
        }
    },
    created() {
        console.log('咨询教师组件创建, RID:', this.rid);
    },
    mounted() {
        console.log('咨询教师组件挂载');
    },
    beforeUnmount() {
        console.log('咨询教师组件销毁');
    }
}
</script>
