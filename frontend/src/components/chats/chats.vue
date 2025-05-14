<template>
    <div>
        <div class="chat">
            <div class="chat-message-body" ref="chatform" @scroll="scroll" v-loading="loading">
                <div v-if="!data || data.length === 0" class="no-messages">
                    <p>暂无消息记录，可以发送消息开始聊天</p>
                </div>
                <div dis-hover v-for="(item, index) in data" :key="index" class="message-card">
                    <div :class="item.isOneself ? 'message-row-right' : 'message-row-left'">
                        <el-avatar 
                            :size="40" 
                            :src="item.avatar || defaultAvatar" 
                            class="avatar" 
                            fit="cover" 
                            round
                        >
                            {{ (item.nickname || '').substring(0, 1) }}
                        </el-avatar>

                        <div class="message-content">
                            <div :style="item.isOneself ? 'text-align:right;display: flex;flex-direction:row-reverse' : ''">
                                <span class="username">{{ item.nickname }}</span>
                                <span class="message-time">
                                    {{ item.addtime }}
                                </span>
                            </div>
                            <div 
                                class="message-body" 
                                :class="{'message-self': item.isOneself}" 
                                v-html="getContent(item.content)"
                            >
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <el-input
                v-model="form.msg"
                type="textarea"
                class="message-input"
                placeholder="请输入消息内容，按Shift+Enter快速发送"
                @keyup.shift.enter="sendMsg"
                :autosize="{ minRows: 3, maxRows: 5 }"
            ></el-input>
        </div>
        <div class="footer-btn">
            <el-button type="primary" @click="sendMsg" :disabled="!form.msg || isLoading">
                <i class="el-icon-s-promotion" v-if="isLoading"></i>
                {{ isLoading ? '发送中...' : '发送' }}
            </el-button>
        </div>
    </div>
</template>


<script>
    import {extend, isObject} from "@/utils/extend";
    import bus from '@/utils/event';
    import avatar from './avatar.jpg';
    import {mapState, mapActions} from 'pinia'
    import {useChatStore} from "@/stores/chat";
    
    export default {
        name: "e-chat",
        props: {
        },
        data() {
            return {
                loading: false,
                isLoading: false,
                defaultAvatar: avatar,
                form: {
                    content: '',
                    msg: ""
                },
            };
        },
        computed: {
            ...mapState(useChatStore, {
                currentChat: (state) => state.currentChat,
                data: (state) => state.currentChat?.data,
            }),
        },
        methods: {
            getContent(html) {
                if (!html) return '';
                return String(html).replace(/[\n]/ig, "<br>");
            },
            scrollToBottom() {
                this.$nextTick(() => {
                    let chatform = this.$refs.chatform;
                    if (chatform) {
                        chatform.scrollTop = chatform.scrollHeight;
                    }
                });
            },
            scroll() {
                if (this.loading) return;
                let chatform = this.$refs.chatform;
                if (chatform) {
                    let scrollTop = chatform.scrollTop;

                    if (scrollTop === 0) {
                        this.loading = true;
                        useChatStore().scrollChatMessage(this.currentChat).then(res => {
                            this.loading = false;
                        });
                        this.$emit('scroll-top');
                    }
                }
            },
            sendMsg() {
                console.log('===== 发送消息过程开始 =====');
                
                if (!this.form.msg) {
                    console.log('消息内容为空，拒绝发送');
                    this.$message.warning("不能发送空白信息");
                    return;
                }
                
                if (this.isLoading) {
                    console.log('上一条消息正在发送中，拒绝重复发送');
                    this.$message.warning("正在发送中，请稍候");
                    return;
                }
                
                if (!this.currentChat) {
                    console.error('聊天会话不存在，无法发送消息');
                    this.$message.error("无法发送消息：会话未初始化");
                    return;
                }
                
                this.isLoading = true;
                
                // 记录相关会话信息供调试
                console.log('当前聊天会话信息:', {
                    chatId: this.currentChat.id,
                    faxinren: this.currentChat.faxinren,
                    shouxinren: this.currentChat.shouxinren,
                    messagesCount: this.data?.length || 0
                });
                
                // 保存消息内容，以防发送失败后恢复
                const messageContent = this.form.msg;
                console.log('待发送消息内容:', messageContent);
                
                // 先清空输入框，给用户更好的响应感
                this.form.msg = '';
                
                try {
                    console.log('调用sendContent方法发送消息');
                    this.sendContent({ 
                        content: messageContent, 
                        chat: this.currentChat 
                    }).then(res => {
                        console.log('消息发送成功', res);
                        this.scrollToBottom();
                        this.isLoading = false;
                        console.log('===== 发送消息过程结束 =====');
                    }).catch(error => {
                        console.error('发送消息失败:', error);
                        // 如果发送失败，恢复消息到输入框
                        this.form.msg = messageContent;
                        
                        // 显示用户友好的错误信息
                        let errorMsg = "发送失败，请重试";
                        let errorDetails = '';
                        
                        if (error && error.message) {
                            errorDetails = error.message;
                            
                            if (error.message.includes('404')) {
                                errorMsg = "消息发送API不存在，请联系管理员";
                                // 记录详细的路径信息以便调试
                                console.error('API路径问题:', { 
                                    message: error.message,
                                    currentUrl: window.location.href,
                                    baseUrl: window.location.origin
                                });
                            } else if (error.message.includes('500')) {
                                errorMsg = "服务器内部错误，请联系管理员";
                            } else if (error.message.includes('401') || error.message.includes('登录')) {
                                errorMsg = "登录已失效，请重新登录";
                            }
                        }
                        
                        // 显示错误信息，包含详细错误信息以便用户报告问题
                        this.$message.error(`${errorMsg} (${errorDetails})`);
                        this.isLoading = false;
                        console.log('===== 发送消息过程结束(失败) =====');
                    });
                } catch (error) {
                    console.error('处理消息发送时出错:', error);
                    // 恢复消息到输入框
                    this.form.msg = messageContent;
                    this.$message.error("发送消息时发生错误");
                    this.isLoading = false;
                    console.log('===== 发送消息过程结束(异常) =====');
                }
            },
            loopChatMessage() {
                this.scrollToBottom();
            },
            ...mapActions(useChatStore, ['sendContent'])
        },
        mounted() {
            bus.on('loopChatMessage', this.loopChatMessage);
            this.scrollToBottom();
        },
        beforeUnmount() {
            bus.off('loopChatMessage', this.loopChatMessage);
        }
    };
</script>

<style lang="scss">
    .chat {
        display: flex;
        flex-direction: column;
        height: 450px;
    }
    
    .chat-message-body {
        background-color: #F8F8F6;
        height: 350px;
        overflow: auto;
        padding: 10px;
        flex: 1;
        
        .no-messages {
            display: flex;
            height: 100%;
            justify-content: center;
            align-items: center;
            color: #999;
            font-size: 14px;
        }
    }
    
    .message-card {
        margin: 8px 0;
        
        .avatar {
            width: 40px;
            height: 40px;
            background-color: #ffffff;
            border-radius: 50%;
            overflow: hidden;
        }
    }
    
    .message-row-left {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    
    .message-row-right {
        display: flex;
        flex-direction: row-reverse;
        align-items: flex-start;
    }
    
    .message-content {
        margin: 0 10px;
        max-width: 70%;
        display: flex;
        flex-direction: column;
        
        .username {
            font-weight: 500;
            font-size: 13px;
        }
    }
    
    .message-body {
        border: 1px solid #EBEEF5;
        padding: 8px 12px;
        border-radius: 4px;
        background-color: #FFF;
        word-break: break-word;
        margin-top: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .message-self {
        background-color: #ecf5ff;
        border-color: #d9ecff;
    }
    
    .message-time {
        margin: 0 5px;
        font-size: 12px;
        color: #909399;
    }
    
    .message-input {
        margin: 10px 0;
    }
    
    .footer-btn {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
</style>
