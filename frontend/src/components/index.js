import { vueGlobalInstall } from "./vue-global";
import Elink from "@/components/ELink.vue";
import ECollect from "./collect.vue";
import EUser from "./EUserInfo.vue";
const modules = import.meta.globEager("./**/index.js");

export function install(app) {
    // 注册全局工具函数
    vueGlobalInstall(app);
    
    // 创建一个已注册组件的集合，防止重复注册
    const registeredComponents = new Set();
    
    // 注册基础组件
    const registerComponent = (name, component) => {
        if (!registeredComponents.has(name)) {
            app.component(name, component);
            registeredComponents.add(name);
        } else {
            console.warn(`组件 "${name}" 已经被注册，跳过重复注册`);
        }
    };
    
    registerComponent("ELink", Elink);
    registerComponent("ECollect", ECollect);
    registerComponent("e-user-info", EUser);

    // 注册模块导出的组件
    for (var module in modules) {
        // 跳过当前模块，避免自循环引用
        if (module === './index.js') continue;
        
        // 创建一个包装器，传递已注册组件集合，以便各模块可以检查
        const moduleInstaller = {
            install: (app) => {
                if (modules[module].default && typeof modules[module].default.install === 'function') {
                    // 传递注册过的组件列表，让子模块可以检查
                    if (modules[module].default._installed) {
                        console.warn(`模块 ${module} 已经被注册，跳过重复注册`);
                        return;
                    }
                    modules[module].default.install(app, registeredComponents);
                    modules[module].default._installed = true;
                }
            }
        };
        
        app.use(moduleInstaller);
    }
}

export default {
    install,
};
