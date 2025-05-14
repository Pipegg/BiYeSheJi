import selectList from "./select-list";
import selectView from "./select-view";
import selectOption from "./select-option";

function install(app, registeredComponents = new Set()) {
    // 检查组件是否已注册，避免重复注册
    const registerComponent = (name, component) => {
        if (!registeredComponents.has(name)) {
            app.component(name, component);
            registeredComponents.add(name);
        } else {
            console.warn(`组件 "${name}" 已经被注册，跳过重复注册`);
        }
    };
    
    registerComponent(selectList.name, selectList);
    registerComponent(selectView.name, selectView);
    registerComponent(selectOption.name, selectOption);
}

export default {
    install,
    selectView,
    selectList,
    selectOption,
};
