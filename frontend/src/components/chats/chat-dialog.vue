<template>
    <el-dialog 
        custom-class="chat-dialog" 
        :title="chat ? (chat.user?.xingming || '聊天内容') : '聊天内容'" 
        v-model="visible" 
        append-to-body 
        width="60%" 
        center 
        :before-close="beforeClose"
        destroy-on-close
    >
        <e-chat-session v-if="visible"></e-chat-session>
    </el-dialog>
</template>
<style lang="scss">
.chat-dialog{
  .el-dialog__body{
    padding: 0!important;
  }
}
</style>
<script>
    import {mapState,mapActions} from 'pinia'
    import {useChatStore} from "@/stores/chat";

export default {
    name: "e-chat-dialog",
    data() {
        return {}
    },
    watch: {},
    computed: {
        ...mapState(useChatStore,{
            chat:(state)=>state.currentChat,
        }),
        visible:{
            get(){
                return useChatStore().visibleModel
            },
            set(val){
                useChatStore().visibleModel = val;
            }
        }
    },
    methods: {
        beforeClose(next){
            useChatStore().selectChat(null);
            next()
        }
    },
    created() {
        console.log("Chat dialog component created");
    },
    mounted() {
        console.log("Chat dialog component mounted");
    },
    destroyed() {
        console.log("Chat dialog component destroyed");
    }
}
</script>
