// 修复聊天消息发送问题的补丁脚本
// 在浏览器控制台中运行此代码以修复聊天功能

(function() {
    console.log('===== 开始应用聊天修复补丁 =====');
    
    if (typeof window.useChatStore !== 'function') {
        console.error('无法找到聊天模块，请确保在正确的页面上运行此脚本');
        return;
    }
    
    // 获取聊天实例
    const chatStore = window.useChatStore();
    
    if (!chatStore) {
        console.error('无法获取聊天实例');
        return;
    }
    
    // 备份原始函数
    const originalSendContent = chatStore.sendContent;
    const originalSendMessageWithFallback = chatStore.sendMessageWithFallback;
    
    // 修复sendContent方法
    chatStore.sendContent = function({ content, chat }) {
        console.log('===== 使用修复版本的sendContent方法 =====');
        
        var userStore = window.useUserStore();
        var session = userStore.session;
        
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
        
        // 构建发送消息的数据，使用确保格式正确的时间字符串
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
            fasongshijian: formattedTime, // 使用格式化的时间字符串
            shifouzhakan: "否",
            siliaoid: siliaoid, // 使用处理后的ID
        };
        
        console.log('准备发送消息:', form);
        
        return new Promise((resolve, reject) => {
            // 先在本地添加一条临时消息，以便立即反馈给用户
            var tempMessage = {
                id: `temp_${Date.now()}`,
                content: content,
                siliaoid: chat.id,
                fasongren: session.username,
                avatar: session.touxiang || '',
                nickname: session.xingming || session.username,
                addtime: form.fasongshijian,
                isOneself: true
            };
            
            // 添加临时消息到UI
            chat.data.push(tempMessage);
            
            // 直接使用不带前缀的API路径，这对于大多数环境应该都是可行的
            const apiUrl = '/xiaoxi/insert/';
            console.log('使用API路径:', apiUrl);
            
            // 使用FormData发送请求
            try {
                const formData = new FormData();
                Object.keys(form).forEach(key => {
                    formData.append(key, form[key]);
                    console.log(`FormData字段: ${key} = ${form[key]}`);
                });
                
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
                    // 检查是否有正确的code字段，或者直接是数据对象
                    if (res.code === 0 || (typeof res.id !== 'undefined')) {
                        var e = res.data || res;
                        e.fasongrenObj = chat.sender;
                        
                        // 移除临时消息
                        const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                        if (tempIndex !== -1) {
                            chat.data.splice(tempIndex, 1);
                        }
                        
                        // 添加服务器返回的消息
                        var data = window.handlerMsg ? window.handlerMsg(e, session, chat) : {
                            id: e.id,
                            content: e.neirong || '',
                            avatar: session.touxiang || '',
                            isOneself: true,
                            addtime: e.fasongshijian || form.fasongshijian,
                            nickname: session.xingming || session.username
                        };
                        
                        // 使用原始commit方法添加消息
                        chatStore.commit('sendContent', { data, session, chat });
                        console.log('消息已添加到聊天中');
                        console.log('===== 修复版本的sendContent方法执行完成 =====');
                        resolve(res);
                    } else {
                        console.error('发送消息服务器返回错误:', res);
                        // 移除临时消息
                        const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                        if (tempIndex !== -1) {
                            chat.data.splice(tempIndex, 1);
                        }
                        reject(new Error(res.msg || '发送失败'));
                    }
                })
                .catch(error => {
                    console.error('消息发送请求失败:', error);
                    // 移除临时消息
                    const tempIndex = chat.data.findIndex(m => m.id === tempMessage.id);
                    if (tempIndex !== -1) {
                        chat.data.splice(tempIndex, 1);
                    }
                    reject(error);
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
    };
    
    console.log('===== 聊天修复补丁已应用 =====');
    console.log('聊天功能现在应该可以正常工作了。');
    console.log('如果还有问题，请尝试刷新页面后重新运行此脚本。');
})(); 