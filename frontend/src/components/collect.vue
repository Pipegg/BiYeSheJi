<template>
    <el-badge :value="collectCount" style="margin-right: 5px">
        <el-button :type="isCollect ? 'danger' : 'primary'" @click="onChangeCollect" :key="componentKey">
            <template #icon>
                <slot name="icon" :isCollect="isCollect">
                    <i :class="isCollect ? 'fa fa-thumbs-up' : 'fa fa-thumbs-o-up'"></i>
                </slot>
            </template>
            <slot :isCollect="isCollect"> {{ isCollect ? successText : notText }} </slot>
        </el-button>
    </el-badge>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";
    import { session } from "@/utils/utils";
    import { ref, reactive, watch, unref, nextTick } from "vue";
    import * as modules from "@/module";
    import { ElMessage } from "element-plus";

    const props = defineProps({
        module: {
            type: String,
        },
        form: Object,
        biao: {
            type: String,
        },
        biaoid: {
            type: String,
        },
        biaoti: {
            type: String,
        },
        successText: {
            type: String,
            default: "",
        },
        notText: {
            type: String,
            default: "",
        },
    });
    const isCollect = ref(false);
    const collectCount = ref(0);

    // 添加componentKey来强制组件刷新
    const componentKey = ref(0);

    // 添加一个标记，指示当前是否正在处理收藏操作
    const isProcessing = ref(false);
    // 添加一个刚刚操作的结果，用于防止立即被覆盖
    const lastOperationResult = ref(null);

    // 创建一个本地存储的键，用于保存收藏状态
    const getStorageKey = () => {
        const username = session("username") || 'guest';
        return `collect_${props.biao}_${props.biaoid}_${username}`;
    };
    
    // 从本地存储加载收藏状态
    const loadFromStorage = () => {
        try {
            const key = getStorageKey();
            const storedState = localStorage.getItem(key);
            if (storedState) {
                const state = JSON.parse(storedState);
                console.log('从本地存储加载收藏状态:', state);
                
                // 只有在没有活动操作时才使用存储的状态
                if (!isProcessing.value && lastOperationResult.value === null) {
                    isCollect.value = !!state.isCollect;
                    collectCount.value = state.collectCount || 0;
                    componentKey.value++; // 刷新组件
                    console.log('已应用本地存储的收藏状态');
                    return true;
                }
            }
        } catch (error) {
            console.error('从本地存储加载状态出错:', error);
        }
        return false;
    };
    
    // 保存收藏状态到本地存储
    const saveToStorage = () => {
        try {
            const key = getStorageKey();
            const state = {
                isCollect: isCollect.value,
                collectCount: collectCount.value,
                timestamp: new Date().getTime()
            };
            localStorage.setItem(key, JSON.stringify(state));
            console.log('收藏状态已保存到本地存储:', state);
        } catch (error) {
            console.error('保存收藏状态到本地存储出错:', error);
        }
    };

    const loadCollect = () => {
        console.log('加载收藏状态，ID:', props.biaoid);
        
        // 确保有用户信息和有效的ID
        const username = session("username");
        if (!username) {
            console.warn('无法获取收藏状态: 用户未登录');
            return;
        }
        
        if (!props.biaoid) {
            console.warn('无法获取收藏状态: 无效的ID');
            return;
        }
        
        // 如果正在处理收藏操作，暂时不重新加载状态
        if (isProcessing.value) {
            console.log('跳过状态加载，因为正在处理收藏操作');
            return;
        }
        
        // 先尝试从本地存储加载
        if (loadFromStorage()) {
            console.log('使用本地存储的状态，跳过API请求');
            return;
        }
        
        var moduleClass = parseName(props.module, 1);
        var biaoClass = parseName(props.biao, 1);
        var createForm = `can${moduleClass}CreateForm`;
        var useGet = `use${biaoClass}${props.module}`;
        console.log('调用获取收藏状态函数:', useGet);
        
        // 检查模块函数是否存在
        if (!modules[useGet]) {
            console.error(`获取收藏状态函数 ${useGet} 不存在`);
            return;
        }
        
        try {
            // 确保ID是字符串格式
            const courseId = String(props.biaoid);
            console.log('处理后的ID用于API调用:', courseId);
            
            // 传递包含显式用户名的参数
            const result = modules[useGet](courseId, isCollect, collectCount);
            console.log('获取收藏状态结果:', result);
            
            // 如果有最近的操作结果，使用它而不是API返回的结果
            if (lastOperationResult.value !== null) {
                console.log('使用最近的操作结果替代API返回值:', lastOperationResult.value);
                isCollect.value = lastOperationResult.value;
                
                // 清除标记
                lastOperationResult.value = null;
                
                // 保存到本地存储
                saveToStorage();
            }
        } catch (error) {
            console.error('获取收藏状态出错:', error);
        }
    };
    
    // 在组件挂载后主动加载一次
    loadCollect();
    
    // 修改收藏操作完成后的处理
    const updateCollectState = () => {
        console.log('更新收藏状态...');
        // 强制刷新组件
        componentKey.value++;
        
        // 重新加载收藏状态
        loadCollect();
        
        // 确保视图更新
        nextTick(() => {
            console.log('收藏状态已更新:', {
                isCollect: isCollect.value,
                collectCount: collectCount.value
            });
        });
    };

    const onChangeCollect = async () => {
        try {
            const username = session("username");
            if (!username) {
                ElMessage.error("请登录后操作");
                // 阻止继续执行
                return;
            }
            
            // 检查ID有效性
            if (!props.biaoid) {
                console.error('无效的收藏ID');
                ElMessage.error("操作失败：无效的参数");
                return;
            }
            
            // 如果正在处理，不允许重复操作
            if (isProcessing.value) {
                console.log('操作被忽略：正在处理前一个请求');
                return;
            }
            
            // 设置处理标志
            isProcessing.value = true;
            
            console.log('执行收藏操作，当前用户:', username);
            console.log('当前收藏状态:', {
                isCollect: isCollect.value,
                collectCount: collectCount.value,
                id: props.biaoid
            });
            
            // 记录即将进行的新状态
            const newCollectState = !isCollect.value;
            
            // 立即预先更新UI状态，提供即时反馈
            isCollect.value = newCollectState;
            collectCount.value = newCollectState ? collectCount.value + 1 : Math.max(0, collectCount.value - 1);
            componentKey.value++; // 刷新组件
            
            // 立即保存到本地存储，确保页面刷新时保持状态
            saveToStorage();
            
            console.log('操作后预期状态:', {
                isCollect: isCollect.value,
                collectCount: collectCount.value
            });
            
            var moduleClass = parseName(props.module, 1);
            var biaoClass = parseName(props.biao, 1);
            var createForm = `can${moduleClass}CreateForm`;
            var insert = `can${moduleClass}Insert`;
            var useGet = `use${biaoClass}${props.module}`;
            
            console.log('使用函数:', {createForm, insert, useGet});
            
            // 检查模块函数是否存在
            if (!modules[createForm] || !modules[insert] || !modules[useGet]) {
                console.error('模块函数不存在:', {
                    createForm: !!modules[createForm],
                    insert: !!modules[insert],
                    useGet: !!modules[useGet]
                });
                ElMessage.error("操作失败：系统配置错误");
                // 还原状态
                isCollect.value = !newCollectState;
                collectCount.value = !newCollectState ? collectCount.value + 1 : Math.max(0, collectCount.value - 1);
                componentKey.value++;
                isProcessing.value = false;
                // 更新本地存储
                saveToStorage();
                return;
            }
            
            var o = props.form;
            
            // 检查表单参数
            if (!o || !o.biaoid || !o.biao || !o.biaoti) {
                console.error('表单参数不完整:', o);
                ElMessage.error("操作失败：参数不完整");
                // 还原状态
                isCollect.value = !newCollectState;
                collectCount.value = !newCollectState ? collectCount.value + 1 : Math.max(0, collectCount.value - 1);
                componentKey.value++;
                isProcessing.value = false;
                // 更新本地存储
                saveToStorage();
                return;
            }
            
            console.log('收藏表单数据:', o);
            
            try {
                // 创建表单
                var { form } = await modules[createForm]();
                
                // 设置表单字段 - 确保ID是字符串
                form[o.biaoid] = String(props.biaoid);
                form[o.biao] = props.biao;
                form[o.biaoti] = props.biaoti;
                // 显式添加用户名
                form['username'] = username;
                
                console.log('准备提交的表单:', form);
                
                // 提交表单
                var s = await modules[insert](form);
                
                console.log('提交结果:', s);
                
                // 处理各种可能的响应格式
                if (typeof s === 'string') {
                    // 如果响应是字符串，尝试解析为JSON
                    console.log('响应是字符串，尝试解析为JSON');
                    try {
                        s = JSON.parse(s);
                    } catch (e) {
                        // 如果不是有效的JSON，创建一个标准格式的对象
                        console.log('非JSON字符串，创建标准对象');
                        s = {
                            code: 0,
                            msg: s,
                            data: { action: s.includes('取消') ? 'cancel' : 'add' }
                        };
                    }
                }
                
                // 特殊处理取消收藏的情况
                if (s && typeof s === 'object' && (s.msg === '已取消收藏' || (s.data && s.data.msg === '已取消收藏'))) {
                    console.log('响应表示取消收藏操作成功');
                    ElMessage.success("取消收藏成功");
                    
                    // 记录操作结果，确保API请求不会覆盖
                    lastOperationResult.value = false; // 取消收藏 = false
                    // 保存到本地存储
                    saveToStorage();
                    
                    // 延迟较长时间后清除处理标志，确保数据同步完成
                    setTimeout(() => {
                        isProcessing.value = false;
                        lastOperationResult.value = null;
                    }, 1000);
                    return;
                }
                
                // 修复响应判断逻辑 - 多种成功判断条件
                if (s && (
                    s.code === 0 || 
                    (s.data && s.data.id) || 
                    s.id ||
                    (typeof s === 'object' && Object.keys(s).length > 0)
                )) {
                    // 检测是创建还是取消
                    const isCancel = s.action === 'cancel' || 
                                    (s.data && s.data.action === 'cancel') ||
                                    (s.msg && s.msg.includes('取消'));
                    
                    // 记录操作结果，确保API请求不会覆盖
                    lastOperationResult.value = !isCancel; // 收藏 = true, 取消 = false
                    // 更新本地存储
                    saveToStorage();
                    
                    // 显示成功提示
                    ElMessage.success(isCancel ? "取消收藏成功" : "收藏成功");
                    
                    // 延迟较长时间后清除处理标志，确保数据同步完成
                    setTimeout(() => {
                        isProcessing.value = false;
                        lastOperationResult.value = null;
                    }, 1000);
                } else {
                    console.error('提交失败:', s);
                    ElMessage.error(s?.msg || "操作失败");
                    
                    // 还原状态
                    isCollect.value = !newCollectState;
                    collectCount.value = !newCollectState ? collectCount.value + 1 : Math.max(0, collectCount.value - 1);
                    componentKey.value++;
                    isProcessing.value = false;
                    // 更新本地存储
                    saveToStorage();
                }
            } catch (error) {
                console.error('收藏操作执行失败:', error);
                ElMessage.error("操作失败：" + (error.message || "未知错误"));
                
                // 还原状态
                isCollect.value = !newCollectState;
                collectCount.value = !newCollectState ? collectCount.value + 1 : Math.max(0, collectCount.value - 1);
                componentKey.value++;
                isProcessing.value = false;
                // 更新本地存储
                saveToStorage();
            }
        } catch (error) {
            console.error('收藏组件错误:', error);
            ElMessage.error("操作处理异常");
            isProcessing.value = false;
        }
    };

    /**
     *
     * @param {string} name
     * @param {number} type
     */
    function parseName(name, type = 0) {
        var str;
        if (type) {
            str = name.replace(/_(a-zA-Z)/i, ($0, $1) => {
                return $1.toLocaleUpperCase();
            });
            return str.substring(0, 1).toLocaleUpperCase() + str.substring(1);
        } else {
            str = name.replace(/[A-Z]/i, ($0) => "_" + $0.toLocaleLowerCase());
            if (str.indexOf("_") === 0) {
                str = str.substring(1);
            }
            return str;
        }
    }

    watch(() => props, loadCollect, { immediate: true, deep: true });
</script>

<style scoped></style>
