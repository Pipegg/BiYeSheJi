import mitt from "mitt";

export const event = mitt();

// 添加安全的事件触发方法，防止事件处理错误导致整个功能中断
export const safeEmit = (eventName, data) => {
    try {
        console.log(`Safely emitting event: ${eventName}`);
        event.emit(eventName, data);
        return true;
    } catch (error) {
        console.error(`Error emitting event ${eventName}:`, error);
        return false;
    }
};

export default event;
