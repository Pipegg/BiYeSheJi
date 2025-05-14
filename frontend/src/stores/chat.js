import http from "@/utils/ajax/http";
import {findIndex, findObject} from "@/utils/utils";
import date from "@/utils/date";
import {isObject, extend, each} from "@/utils/extend";
import {updateChat,handlerMsg} from '@/components/chats/utils'
import rule from "@/utils/rule";
import bus from '@/utils/event'
import { defineStore } from "pinia";
import {useUserStore} from "@/stores/user";

const state = {
    // 会话列表
    currentSessionTime:'',
    sessionList:[],
    currentChat:null,
    status:false,
    visibleModel:false
};

var timer;
var timeout = 10 * 1000;
var chatMessageTime = 5 * 1000;


const mutations = {
    showModel(state){
        console.log('显示聊天对话框');
        state.visibleModel = true;
    },
    hideModel(state){
        console.log('隐藏聊天对话框');
        state.visibleModel = false;
    },
    setModel(state,val){
        console.log('设置聊天对话框可见性:', val);
        state.visibleModel = val;
    },
    sendContent(state,{data,session,chat}){
        chat.distincData.push(data.id);
        chat.data.push(data);
        if(chat.offsetMax < data.id){
            chat.offsetMax = data.id;
        }
    },
    scrollChatMessage(state,{list,session,chat}){
        list.forEach(e=>{
            if(chat.distincData.indexOf(e.id) <0){
                var data = handlerMsg(e,session,chat);
                chat.data.unshift(data);
                chat.distincData.push(e.id);
                // 修改最小偏移位
                if(chat.offsetMin > e.id){
                    chat.offsetMin = e.id;
                }
            }
        });
    },
    clearSessionList(state){
        state.sessionList = [];
        state.currentChat = null;
    },
    oneChatMessage(state,{list,session}){
        var chat = state.currentChat;
        list.forEach(e=>{
            if(state.currentChat.id == e.siliaoid){
                if(chat.offsetMax < e.id){
                    chat.offsetMax = e.id;
                }
                if(chat.distincData.indexOf(e.id) == -1){
                    var data = handlerMsg(e,session,state.currentChat);
                    chat.distincData.push(e.id);
                    chat.data.unshift(data);
                    //if(chat.offsetMin > e.id){
                    chat.offsetMin = e.id;

                }
            }
        });
        bus.emit('loopChatMessage');
    },
    loopChatMessage( state,{list,session} ){
        var chat = state.currentChat;
        list = list.reverse();
        list.forEach(e=>{
            if(state.currentChat.id == e.siliaoid){
                if(chat.offsetMax < e.id){
                    chat.offsetMax = e.id;
                }
                if(chat.distincData.indexOf(e.id) == -1){
                    var data = handlerMsg(e,session,state.currentChat);
                    chat.distincData.push(e.id);
                    chat.data.push(data);
                }
            }
        });
        bus.emit('loopChatMessage');
    },
    clearChat(state){
        for (var co of state.sessionList){
            if(co.timer){
                clearTimeout(co.timer);
                co.timer = null;
            }
        }
    },
    updateChat(state , chat){
        state.currentChat = chat;
    },
    setList(state,list){
        for (var co of list){
            updateChat(co);
        }
        if(list.length > 0){
            state.currentSessionTime = list[list.length-1].addtime;
        }else{
            state.currentSessionTime = date("Y-m-d H:i:s");
        }
        state.sessionList = list.sort((a,b)=>{
            if(b.addtime == a.addtime){
                return 0;
            }
            return b.addtime > a.addtime ? 1 : -1;
        });

    },
    updateList(state,list){
        for (var co of list){
            var index = findIndex(state.sessionList , r=>r.id == co.id);
            if(index !== false){
                var newData = state.sessionList.splice(index , 1)[0];
                newData.readCount = co.readCount;
                state.sessionList.unshift(newData);
            }else{
                updateChat(co);
                state.sessionList.unshift(co);
            }
            state.currentSessionTime = co.xiaoxizuihoushijian;
        }
    }
};

const actions = {
    updateSessionList(data){
        return new Promise((resolve, reject) => {
            if(data.type == 'new'){
                data.lastdate = this.currentSessionTime || '';
            }
            
            // 确保数据格式正确
            const requestData = {
                sid: data.sid || '',
                type: data.type || 'one',
                lastdate: data.lastdate || ''
            };
            
            console.log('发送会话列表请求:', requestData);
            
            // 添加错误处理
            try {
                // 将对象序列化为JSON字符串
                const jsonData = JSON.stringify(requestData);
                console.log('发送JSON数据:', jsonData);
                
                // 设置正确的请求配置
                const requestOptions = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    },
                    body: jsonData,
                    credentials: 'include',
                    mode: 'cors',
                    cache: 'no-cache'
                };
                
                // 使用fetch API发送请求
                fetch("/api/chat/sessionList/", requestOptions)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(res => {
                    console.log('会话列表响应:', res);
                    
                    if(res.code == 0){
                        if(data.type == 'one'){
                            mutations.setList(this, res.data || []);
                        }else if(data.type == 'new'){
                            mutations.updateList(this, res.data || []);
                        }
                    }
                    resolve(res);
                })
                .catch(error => {
                    console.error('聊天会话列表请求失败:', error);
                    resolve({ code: -1, msg: '聊天会话列表获取失败: ' + (error.message || '未知错误') });
                });
            } catch(e) {
                console.error('执行聊天会话列表请求时出错:', e);
                resolve({ code: -1, msg: '聊天会话列表请求出错: ' + e.message });
            }
        });
    },
    commit(action,data){
        if(mutations[action]){
            mutations[action](this,data);
        }
    },
    dispatch(action,data){
        if(this[action]){
            return this[action].call(this,data);
        }
        return null;
    },
    check({sid,rid}){
        return new Promise((resolve, reject) => {
            try {
                console.log(`创建聊天会话: 学生=${sid}, 教师=${rid}`);
                
                if (!sid || !rid) {
                    console.error('缺少必要的用户ID信息');
                    return reject(new Error('缺少用户ID信息'));
                }
                
                // 直接创建会话对象
                var siliao = {
                    id: new Date().getTime(), // 使用时间戳作为ID
                    faxinren: sid,
                    shouxinren: rid,
                    bianhao: `CHAT${new Date().getTime()}`,
                    addtime: new Date().toISOString().slice(0, 19).replace('T', ' ')
                };
                
                // 更新UI，就像从API获取一样
                return this.updateSessionList({
                    sid: sid,
                    type: 'new'
                }).then(r => {
                    // 检查会话列表中是否已存在该会话
                    var chat = findObject(this.sessionList, r => r.id == siliao.id);
                    
                    // 如果在会话列表中未找到，手动添加
                    if (!chat) {
                        console.log('在会话列表中未找到该聊天，手动添加');
                        
                        // 创建有效的聊天对象
                        chat = {
                            id: siliao.id,
                            faxinren: siliao.faxinren,
                            shouxinren: siliao.shouxinren,
                            bianhao: siliao.bianhao,
                            addtime: siliao.addtime,
                            readCount: 0,
                            distincData: [],
                            data: [],
                            offsetMin: 100000000,
                            offsetMax: 0
                        };
                        
                        // 尝试添加用户信息（如果可用）
                        try {
                            // 在现有会话中查找包含相同用户的会话
                            const otherUser = findObject(this.sessionList, r => 
                                r.shouxinren === rid || r.faxinren === rid);
                            
                            if (otherUser && otherUser.user) {
                                console.log('从现有会话复制用户信息');
                                chat.user = otherUser.user;
                            } else {
                                console.log('无法找到用户信息，使用默认值');
                                // 设置默认用户信息
                                chat.user = {
                                    xingming: '教师', // 默认名称
                                    touxiang: '' // 默认头像留空
                                };
                            }
                        } catch(e) {
                            console.warn('获取用户信息失败:', e);
                            // 设置默认用户信息
                            chat.user = {
                                xingming: '教师', // 默认名称
                                touxiang: '' // 默认头像留空
                            };
                        }
                        
                        // 添加到会话列表
                        this.sessionList.unshift(chat);
                    } else {
                        console.log('找到现有聊天会话:', chat.id);
                    }
                    
                    // 选择聊天并显示对话框
                    this.selectChat(chat);
                    
                    // 确保对话框可见
                    console.log('打开聊天对话框');
                    mutations.showModel(this);
                    
                    // 延迟200ms后再次确认对话框已打开
                    setTimeout(() => {
                        if (!this.visibleModel) {
                            console.log('对话框未正确打开，重试...');
                            mutations.showModel(this);
                        }
                    }, 200);
                    
                    resolve(chat);
                }).catch(error => {
                    console.error('创建聊天会话失败:', error);
                    reject(error);
                });
            } catch (error) {
                console.error('处理聊天会话时出错:', error);
                reject(error);
            }
        });
    },
    login()
    {
        var userStore = useUserStore();
        var session = userStore.session;
        
        if (!session || !session.username) {
            console.error('登录聊天失败: 没有有效的会话数据');
            return Promise.resolve({ code: -1, msg: '没有有效的用户数据' });
        }
        
        console.log('聊天模块登录，用户:', session.username);
        
        // 直接初始化聊天
        return this.updateSessionList({
            sid: session.username,
            type: 'one'
        }).then(res => {
            console.log('聊天会话列表获取成功，设置轮询');
            this.status = true;
            this.loopUpdateSessionList();
            return { code: 0, msg: '聊天初始化成功' };
        }).catch(error => {
            console.error('聊天初始化失败:', error);
            return { code: -1, msg: '聊天初始化失败: ' + (error.message || '未知错误') };
        });
    },
    logout(){
        if(this.status){
            this.status = false;
            clearTimeout(timer);
            this.commit('clearChat');
            this.commit('clearSessionList');
        }
    },
    loopUpdateSessionList(){
        return new Promise((resolve, reject) => {
            if (!this.status) {
                console.log('聊天模块未启动，不进行轮询');
                resolve({ code: -1, msg: '聊天模块未启动' });
                return;
            }
            
            var userStore = useUserStore();
            var session = userStore.session;
            
            if (!session || !session.username) {
                console.warn('轮询时没有有效的会话数据');
                if (this.status) {
                    timer = setTimeout(() => {
                        this.loopUpdateSessionList();
                    }, timeout);
                }
                resolve({ code: -1, msg: '没有有效的用户数据' });
                return;
            }
            
            this.updateSessionList({
                sid: session.username,
                type: 'new'
            }).then(res => {
                // 无论结果如何都继续轮询
                if (this.status) {
                    timer = setTimeout(() => {
                        this.loopUpdateSessionList();
                    }, timeout);
                }
                resolve(res);
            }).catch(error => {
                console.error('轮询聊天列表失败:', error);
                // 即使出错也继续轮询
                if (this.status) {
                    timer = setTimeout(() => {
                        this.loopUpdateSessionList();
                    }, timeout);
                }
                resolve({ code: -1, msg: '轮询失败: ' + (error.message || '未知错误') });
            });
        });
    },
    selectChat( chat ){
        this.commit('clearChat');
        this.commit('updateChat' , chat);
        if(chat && chat.id){
            if(chat.loading == 'loop'){
                // 则继续，
                this.loopChatMessage(chat);
            }else{
                this.oneChatMessage(chat);
            }
            var userStore = useUserStore();
            var session = userStore.session;
            this.updateRead({chat,sid:session.username});
        }
    },
    updateRead({chat,sid}){
        console.log(`正在更新聊天已读状态: chatid=${chat.id}, sid=${sid}`);
        
        try {
            // 确保参数都是字符串类型
            const chatid = String(chat.id);
            const sidStr = String(sid);
            
            // 构建表单数据
            const formData = new FormData();
            formData.append('chatid', chatid);
            formData.append('sid', sidStr);
            console.log('使用FormData发送请求');
            
            // 使用fetch API发送表单数据
            return fetch("/api/chat/updateRead/", {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData,
                credentials: 'include'
            })
            .then(response => {
                console.log(`响应状态: ${response.status} ${response.statusText}`);
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('更新聊天已读状态成功:', data);
                chat.readCount = 0;
                return data;
            })
            .catch(error => {
                console.error('更新聊天已读状态失败:', error);
                // 即使出错也将消息标记为已读，以避免重复通知用户
                chat.readCount = 0;
            });
        } catch (e) {
            console.error('执行更新聊天已读状态请求时出错:', e);
            // 出错也标记为已读
            chat.readCount = 0;
        }
    },
    sendContent({ content, chat }) {
        var userStore = useUserStore();
        var session = userStore.session;
        
        console.log('===== DEBUG: 开始发送消息 =====');
        console.log('会话信息:', { chatId: chat?.id, userId: session?.username });
        
        // 验证必要参数
        if (!content || !chat || !chat.id) {
            console.error('发送消息参数不完整:', { content, chatId: chat?.id });
            return Promise.reject(new Error('消息参数不完整'));
        }
        
        // 验证会话数据
        if (!session || !session.username) {
            console.error('缺少用户会话信息');
            return Promise.reject(new Error('用户未登录'));
        }
        
        // 处理siliaoid为较小的整数，避免超出数据库范围
        let siliaoid;
        try {
            // 尝试使用原始ID的最后9位数字，这通常在数据库整数范围内
            const idStr = String(chat.id);
            if (idStr.length > 9) {
                siliaoid = parseInt(idStr.slice(-9));
            } else {
                siliaoid = parseInt(idStr);
            }
            // 如果解析失败或结果为NaN，则使用较小的数值
            if (isNaN(siliaoid) || siliaoid <= 0) {
                siliaoid = Math.floor(Math.random() * 1000000) + 1; // 1 到 1,000,000 之间的随机数
            }
            console.log(`将会话ID ${chat.id} 处理为数据库兼容的ID: ${siliaoid}`);
        } catch (e) {
            console.error('处理会话ID时出错:', e);
            siliaoid = Math.floor(Math.random() * 1000000) + 1;
        }
        
        // 构建发送消息的数据 - 确保日期格式正确
        const currentTime = new Date();
        const formattedTime = currentTime.getFullYear() + '-' + 
            String(currentTime.getMonth() + 1).padStart(2, '0') + '-' + 
            String(currentTime.getDate()).padStart(2, '0') + ' ' + 
            String(currentTime.getHours()).padStart(2, '0') + ':' + 
            String(currentTime.getMinutes()).padStart(2, '0') + ':' + 
            String(currentTime.getSeconds()).padStart(2, '0');
            
        var form = {
            neirong: content,
            fasongren: session.username,
            fasongshijian: formattedTime, // 使用确保格式正确的时间字符串
            shifouzhakan: "否",
            siliaoid: siliaoid, // 使用处理后的ID
        };
        
        console.log('准备发送消息:', form);
        
        return new Promise((resolve, reject) => {
            // 先在本地添加一条临时消息，以便立即反馈给用户
            var tempMessage = {
                id: `temp_${Date.now()}`,
                content: content,
                siliaoid: chat.id, // 前端UI中仍使用原始ID
                fasongren: session.username,
                avatar: session.touxiang || '',
                nickname: session.xingming || session.username,
                addtime: form.fasongshijian,
                isOneself: true
            };
            
            // 添加临时消息到UI
            chat.data.push(tempMessage);
            
            // 先尝试带前缀的API路径，这在当前环境下是可行的
            const apiUrl = '/api/xiaoxi/insert/';
            console.log('使用API路径:', apiUrl);
            
            // 使用FormData发送请求，避免潜在的内容类型问题
            try {
                const formData = new FormData();
                Object.keys(form).forEach(key => {
                    formData.append(key, form[key]);
                    console.log(`FormData字段: ${key} = ${form[key]}`);
                });
                
                console.log('发送请求到:', apiUrl);
                
                fetch(apiUrl, {
                    method: 'POST',
                    body: formData,
                    credentials: 'include',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    console.log('收到服务器响应:', response.status, response.statusText);
                    if (!response.ok) {
                        throw new Error(`服务器响应错误: ${response.status} ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(res => {
                    console.log('消息发送成功, 服务器响应:', res);
                    if (res.code === 0 || (typeof res.id !== 'undefined')) {
                        var e = res.data || res;
                        e.fasongrenObj = chat.sender;
                        
                        // 移除临时消息
                        const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                        if (tempIndex !== -1) {
                            chat.data.splice(tempIndex, 1);
                        }
                        
                        // 添加服务器返回的消息
                        var data = handlerMsg(e, session, chat);
                        this.commit('sendContent', { data, session, chat });
                        console.log('消息已添加到聊天中');
                        console.log('===== DEBUG: 发送消息完成 =====');
                        resolve(res);
                    } else {
                        console.error('发送消息服务器返回错误:', res);
                        // 移除临时消息
                        const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                        if (tempIndex !== -1) {
                            chat.data.splice(tempIndex, 1);
                        }
                        // 尝试使用带有/api前缀的API路径
                        this.sendMessageWithFallback(form, tempMessage, chat, session, resolve, reject);
                    }
                })
                .catch(error => {
                    console.error('消息发送请求失败:', error);
                    // 尝试使用带有/api前缀的API路径
                    console.log('尝试使用备用路径发送消息...');
                    this.sendMessageWithFallback(form, tempMessage, chat, session, resolve, reject);
                });
            } catch (error) {
                console.error('发送消息出现异常:', error);
                // 移除临时消息
                const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                if (tempIndex !== -1) {
                    chat.data.splice(tempIndex, 1);
                }
                reject(error);
            }
        });
    },
    sendMessageWithFallback(form, tempMessage, chat, session, resolve, reject) {
        // 备用路径不带 /api 前缀
        const fallbackUrl = '/xiaoxi/insert/';
        console.log('使用备用API路径:', fallbackUrl);
        
        try {
            // 使用Axios库发送，确保兼容性
            http.post(fallbackUrl, form).json().then(res => {
                console.log('备用路径发送成功, 服务器响应:', res);
                // 检查是否有正确的code字段，code应该为0表示成功
                // 注意：有些API可能直接返回数据对象而不是包装在code/data结构中
                if (res && (res.code === 0 || (typeof res.id !== 'undefined'))) {
                    var e = res.data || res; // 如果res本身就是数据，则直接使用
                    e.fasongrenObj = chat.sender;
                    
                    // 移除临时消息
                    const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                    if (tempIndex !== -1) {
                        chat.data.splice(tempIndex, 1);
                    }
                    
                    // 添加服务器返回的消息
                    var data = handlerMsg(e, session, chat);
                    this.commit('sendContent', { data, session, chat });
                    console.log('消息已添加到聊天中');
                    console.log('===== DEBUG: 备用路径发送消息完成 =====');
                    resolve(res);
                } else {
                    console.error('备用路径发送消息服务器返回错误:', res);
                    // 移除临时消息
                    const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                    if (tempIndex !== -1) {
                        chat.data.splice(tempIndex, 1);
                    }
                    reject(new Error(res.msg || '发送失败'));
                }
            }).catch(error => {
                console.error('备用路径消息发送失败:', error);
                // 移除临时消息
                const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                if (tempIndex !== -1) {
                    chat.data.splice(tempIndex, 1);
                }
                reject(error);
            });
        } catch (error) {
            console.error('备用路径发送消息异常:', error);
            // 移除临时消息
            const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
            if (tempIndex !== -1) {
                chat.data.splice(tempIndex, 1);
            }
            reject(error);
        }
    },
    scrollChatMessage(chat)
    {
        return new Promise((resolve, reject) => {
            var form = {
                chatid:chat.id,
                offsetMin:chat.offsetMin,
                type:'top'
            };

            http.post('/api/chat/chatMessage/',form).json().then(res=>{
                var userStore = useUserStore();
                var session = userStore.session;

                this.commit('scrollChatMessage' , {
                    list:res.data,
                    session:session,
                    chat:chat
                });
                resolve(res);
            },reject);
        });
    },
    oneChatMessage(chat){
        if(chat.loading === 'loading'){
            chat.loading = 'one';
            var form = {
                pageSize:20,
                pageNumber:1,
                offsetMax:chat.offsetMax,
                type:'one',
                chatid:chat.id
            };
            http.post('/api/chat/chatMessage/',form).json().then(res=>{
                var userStore = useUserStore();
                var $session = userStore.session;

                this.commit('oneChatMessage' , {
                    list:res.data,
                    session:$session
                });
                chat.loading = 'loop';
                this.currentChat.timer = setTimeout(()=>{
                    this.loopChatMessage()
                },chatMessageTime);
            });
        }
    },
    loopChatMessage(){
        if(!this.status)return;
        var chat = this.currentChat;
        let params = {};
        params.pageNumber = 1;
        params.pageSize = 20;
        params.offsetMax = chat.offsetMax;
        params.type = "new";
        params.chatid = chat.id;
        http.post('/api/chat/chatMessage/' , params).json().then(res=>{
            if(res.code == 0){
                var userStore = useUserStore();
                var $session = userStore.session;
                // 数据转换
                //var result = [];

                // 发信人
                //var chat = content.state.currentChat;
                if(res.data.length > 0){
                    this.commit('loopChatMessage' , {
                        list:res.data,
                        session:$session
                    });
                    this.updateRead({chat,sid:$session.username});
                }

                this.currentChat.timer = setTimeout(()=>{
                    this.loopChatMessage();
                },chatMessageTime);
            }
        });
    },
};

each(mutations,(key,mutation)=>{
    var k = 'SET_'+key;
    actions[k] = function(data){
        mutation.call(this,this,data);
    }
});


export const useChatStore = defineStore("chat",{
    state(){
        return extend({},state);
    },
    getters:{
        readCount:state=>{
            var readCount = 0;
            for (var co of state.sessionList){
                readCount += co.readCount;
            }
            return readCount;
        }
    },
    actions:actions
});
