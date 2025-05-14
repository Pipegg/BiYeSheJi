<template>
    <div class="session-box">
        <div class="session-list">
            <div v-if="sessionList.length === 0" class="empty-sessions">
                <p>暂无聊天记录</p>
            </div>
            <div 
                class="session-chat" 
                v-for="v in sessionList" 
                :class="{active: chat && v.id === chat.id}" 
                :key="v.id" 
                @click="selectChat(v)"
            >
                <div class="session">
                    <div class="headimgurl">
                        <el-avatar :size="40" :src="v.user?.touxiang || defaultAvatar">
                            {{ (v.user?.xingming || '未知').substring(0, 1) }}
                        </el-avatar>
                    </div>
                    <div class="username">
                        <div class="name">
                            <div class="">{{ v.user?.xingming || '未知用户' }}</div>
                            <div class="">
                                <el-badge v-show="v.readCount>0" :value="v.readCount" :max="99" class="item"></el-badge>
                            </div>
                        </div>
                        <div class="time">{{ v.addtime }}</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="session-content">
            <template v-if="chat">
                <div class="session-siliao-item">
                    <e-chat></e-chat>
                </div>
            </template>
            <div v-else class="no-selected-chat">
                <p>请选择一个聊天会话</p>
            </div>
        </div>
    </div>
</template>

<script>
    import {extend, isObject} from "@/utils/extend";
    import rule from "@/utils/rule";
    import {mapState, mapActions} from 'pinia'
    import {useChatStore} from "@/stores/chat";
    import defaultAvatar from './avatar.jpg';

    export default {
        name: "e-chat-session",
        data() {
            return {
                defaultAvatar
            };
        },
        computed:{
            ...mapState(useChatStore,{
                sessionList:(state)=>state.sessionList,
                chat:(state)=>state.currentChat,
            }),
        },
        methods: {
            ...mapActions(useChatStore,['selectChat']),
        },
        mounted() {
            console.log("聊天会话列表:", JSON.parse(JSON.stringify(this.sessionList)));
        }
    };
</script>

<style lang="scss">
    .session-box{
        display: flex;
        font-size: 14px;
        height: 550px;
        .session-list{
            flex-grow: 0;
            flex-shrink: 0;
            width: 200px;
            padding: 10px;
            border-right: 1px solid #DEDEDE;
            overflow: hidden;
            overflow-y: auto;
            .empty-sessions {
                text-align: center;
                color: #999;
                padding: 20px 0;
            }
            .session-chat{
                padding: 8px;
                transition: all 0.2s;
                border-radius: 4px;
                margin-bottom: 8px;
                cursor: pointer;
                &:hover {
                    background-color: #f5f5f5;
                }
            }
            .session{
                display: flex;
                min-height: 40px;
                .headimgurl{
                    width: 40px;
                    margin-right: 10px;
                    flex-grow: 0;
                    flex-shrink: 0;
                }
                .username{
                    flex-grow: 1;
                    flex-shrink: 1;
                    display: flex;
                    flex-flow: column;
                    justify-content: space-between;
                    .name{
                        display: flex;
                        justify-content: space-between;
                        font-weight: 500;
                    }
                    .time{
                        font-size: 11px;
                        color: #999;
                        margin-top: 4px;
                    }
                }
            }
            .session-chat.active{
                background: #e6f1fc;
            }
        }
        .session-content{
            flex-grow: 1;
            flex-shrink: 1;
            padding: 10px;
            
            .no-selected-chat {
                display: flex;
                height: 100%;
                justify-content: center;
                align-items: center;
                color: #999;
                font-size: 16px;
            }
        }
    }
</style>
