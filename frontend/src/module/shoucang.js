import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

/**
 * 响应式的对象数据
 */

export const ShoucangCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        xwid: route.query?.xwid,
        biao: route.query?.biao,
        biaoti: route.query?.biaoti,
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canShoucangCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = ShoucangCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取收藏 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useShoucangCreateForm = () => {
    const form = ShoucangCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canShoucangSelect = (filter, result) => {
    http.post("/shoucang/index/").then((res) => {
        if (res.code == 0) {
            extend(result, res.data);
        } else {
            ElMessageBox.alert(res.msg);
        }
    });
};

/**
 * 获取分页数据
 * @param filter
 */
export const useShoucangSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canShoucangSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canShoucangFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/shoucang/findById/", { id }).then((res) => {
            if (res.code == 0) {
                resolve(res.data);
            } else {
                reject(new Error(res.msg));
            }
        }, reject);
    });
};

/**
 * 根据id 获取一行数据
 * @param id
 * @return {UnwrapNestedRefs<{}>}
 */
export const useShoucangFindById = (id) => {
    var form = reactive({});

    canShoucangFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canShoucangInsert = (data) => {
    const userStore = useUserStore();
    const session = userStore.session;
    
    return new Promise((resolve, reject) => {
        console.log('执行收藏操作，数据:', data);
        console.log('当前用户信息:', {
            hasSession: !!session,
            username: session?.username,
            token: userStore.token ? '有效' : '无效'
        });
        
        // 确保数据中包含用户名
        if (!data.username && session && session.username) {
            data.username = session.username;
            console.log('已添加用户名到请求数据:', data);
        }
        
        // 构建请求配置
        const requestConfig = {
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        // 添加认证信息
        if (userStore.token) {
            requestConfig.headers['Authorization'] = `Bearer ${userStore.token}`;
            requestConfig.headers['token'] = userStore.token;
            console.log('已添加认证头');
        }
        
        http.post("/shoucang/insert/", data, requestConfig)
            .json()
            .then(
                (res) => {
                    console.log('收藏操作响应:', res);
                    
                    // 处理字符串响应
                    if (typeof res === 'string') {
                        console.log('响应是字符串:', res);
                        // 尝试解析为JSON
                        try {
                            res = JSON.parse(res);
                            console.log('已解析字符串为JSON:', res);
                        } catch (e) {
                            // 创建标准响应对象
                            console.log('构建标准响应对象');
                            const isCancel = res.includes('取消');
                            res = {
                                code: 0,
                                msg: res,
                                data: {
                                    action: isCancel ? 'cancel' : 'add',
                                    username: data.username,
                                    xwid: data.xwid,
                                    biao: data.biao,
                                    biaoti: data.biaoti
                                }
                            };
                        }
                    }
                    
                    // 检查响应是否有效，支持多种格式
                    const isSuccess = res && (
                        res.code === 0 || // 标准成功响应
                        res.id || // 直接返回对象
                        (res.data && res.data.id) || // 标准格式中的数据
                        (typeof res === 'object' && Object.keys(res).length > 0) // 任何非空对象
                    );
                    
                    if (isSuccess) {
                        console.log('收藏操作成功');
                        
                        // 标准化响应格式
                        const normalizedResponse = {
                            code: 0,
                            msg: res.msg || (res.id ? '操作成功' : ''),
                            data: res.data || res
                        };
                        
                        // 触发事件
                        event.emit("shoucang_insert", normalizedResponse.data);
                        event.emit("shoucang_change", normalizedResponse.data);
                        
                        // 返回标准化响应
                        resolve(normalizedResponse);
                    } else {
                        console.error('收藏操作返回未识别的格式:', res);
                        resolve(res); // 仍然返回原始响应
                    }
                },
                (err) => {
                    console.error('收藏操作失败:', err);
                    reject(err);
                }
            );
    });
};

/**
 * 根据数据更新数据库
 * @param data
 * @return {Promise<unknown>}
 */
export const canShoucangUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/shoucang/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("shoucang_update", res.data);
                        event.emit("shoucang_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

/**
 * 根据id 或者列表id
 * @param id
 * @return {Promise<unknown>}
 */
export const canShoucangDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/shoucang/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("shoucang_delete", res.data);
                        event.emit("shoucang_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
