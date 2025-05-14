import EContainer from "./container.vue";
import EModuleInfo from "./module-info.vue";

const install = (app, registeredComponents = new Set()) => {
    // 检查组件是否已注册，避免重复注册
    const registerComponent = (name, component) => {
        if (!registeredComponents.has(name)) {
            app.component(name, component);
            registeredComponents.add(name);
        } else {
            console.warn(`组件 "${name}" 已经被注册，跳过重复注册`);
        }
    };
    
    registerComponent(EContainer.name, EContainer);
    registerComponent(EModuleInfo.name, EModuleInfo);
};

export default {
    install,
    EContainer,
};
