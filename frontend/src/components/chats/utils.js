import {isObject} from "@/utils/extend";
import {formatImageSrc} from "@/utils/utils";
import defaultAvatar from './avatar.jpg';

// 处理头像URL，提供默认头像和错误处理
function getAvatarUrl(avatarPath) {
    if (!avatarPath) {
        console.log('使用默认头像 (路径为空)');
        return defaultAvatar;
    }
    
    try {
        // 检查是否为完整URL
        if (avatarPath.startsWith('http://') || avatarPath.startsWith('https://')) {
            return avatarPath;
        }
        
        // 使用formatImageSrc格式化路径，如果出错则使用默认头像
        const formattedPath = formatImageSrc(avatarPath);
        if (!formattedPath || formattedPath.includes('undefined')) {
            console.log(`头像路径无效: ${avatarPath}, 使用默认头像`);
            return defaultAvatar;
        }
        
        return formattedPath;
    } catch (error) {
        console.error('处理头像URL时出错:', error);
        return defaultAvatar;
    }
}

export function updateChat(chat) {
    chat.loading = 'loading';
    chat.data = [];
    chat.timer = null;
    chat.distincData = [];
    chat.offsetMax = 0;
    chat.offsetMin = 0;
    chat.searchForm = {
        pageNumber: 1,
        pageSize: 20
    };
}

export function handlerMsg(e, session, chat) {
    // 安全地获取发送者对象，防止未定义错误
    const sender = e.fasongrenObj || {};
    
    // 判断消息是否由当前用户发送
    const isCurrentUser = e.fasongren === session.username;
    
    // 使用适当的昵称，提供回退选项
    const nickname = sender.xingming || e.fasongren || '未知用户';
    
    // 处理头像路径
    const avatarPath = isCurrentUser ? (session.touxiang || '') : (sender.touxiang || '');
    const avatar = getAvatarUrl(avatarPath);
    
    console.log(`处理消息: ID=${e.id}, 发送人=${e.fasongren}, 是否自己=${isCurrentUser}, 头像=${avatar !== defaultAvatar ? '有自定义头像' : '使用默认头像'}`);
    
    return {
        id: e.id,
        content: e.neirong || '',
        avatar: avatar,
        isOneself: isCurrentUser,
        addtime: e.fasongshijian || new Date().toLocaleString(),
        nickname: nickname
    };
}

export default {
    handlerMsg,
    updateChat,
    getAvatarUrl
}
