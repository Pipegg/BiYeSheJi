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

export const LuntanfenleiCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        fenleimingcheng: "",
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canLuntanfenleiCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = LuntanfenleiCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取论坛分类 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useLuntanfenleiCreateForm = () => {
    const form = LuntanfenleiCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canLuntanfenleiSelect = (filter, result) => {
    http.post("/luntanfenlei/index/").then((res) => {
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
export const useLuntanfenleiSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canLuntanfenleiSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canLuntanfenleiFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/luntanfenlei/findById/", { id }).then((res) => {
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
export const useLuntanfenleiFindById = (id) => {
    var form = reactive({});

    canLuntanfenleiFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canLuntanfenleiInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/luntanfenlei/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanfenlei_insert", res.data);
                        event.emit("luntanfenlei_change", res.data);
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
export const canLuntanfenleiUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/luntanfenlei/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanfenlei_update", res.data);
                        event.emit("luntanfenlei_change", res.data);
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
export const canLuntanfenleiDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/luntanfenlei/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanfenlei_delete", res.data);
                        event.emit("luntanfenlei_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
