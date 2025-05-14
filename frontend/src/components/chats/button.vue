<template>
    <span @click="showModel">
        消息 {{ readCount }}
    </span>
</template>

<script>
import {mapState,mapActions} from 'pinia'
import {useChatStore} from "@/stores/chat";

export default {
    name: "e-chat-button",
    data(){
        return {
            visible:false
        }
    },
    computed:{
        ...mapState(useChatStore , {
            readCount:'readCount'
        })
    },
    methods:{
        beforeClose(){
            return true;
        },
        showModel(){
            this.SET_showModel();
        },
        ...mapActions(useChatStore,['SET_showModel']),
    }
}
</script>

<style scoped>

</style>
