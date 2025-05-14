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

export const JiaoshiCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        gonghao: "",
        mima: "",
        xingming: "",
        xingbie: "",
        zhicheng: "",
        lianxifangshi: "",
        youxiang: "",
        touxiang: "",
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canJiaoshiCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = JiaoshiCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取教师 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useJiaoshiCreateForm = () => {
    const form = JiaoshiCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canJiaoshiSelect = (filter, result) => {
    http.post("/jiaoshi/index/").then((res) => {
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
export const useJiaoshiSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canJiaoshiSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canJiaoshiFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/jiaoshi/findById/", { id }).then((res) => {
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
export const useJiaoshiFindById = (id) => {
    var form = reactive({});

    canJiaoshiFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canJiaoshiInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/jiaoshi/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoshi_insert", res.data);
                        event.emit("jiaoshi_change", res.data);
                    }
                },
                (err) => {
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
export const canJiaoshiUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/jiaoshi/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoshi_update", res.data);
                        event.emit("jiaoshi_change", res.data);
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
export const canJiaoshiDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/jiaoshi/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoshi_delete", res.data);
                        event.emit("jiaoshi_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
