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

export const AdminsCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        username: "",
        pwd: "",
        xingming: "",
        xingbie: "",
        lianxifangshi: "",
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
export const canAdminsCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = AdminsCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取管理员 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useAdminsCreateForm = () => {
    const form = AdminsCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canAdminsSelect = (filter, result) => {
    http.post("/admins/index/").then((res) => {
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
export const useAdminsSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canAdminsSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canAdminsFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/admins/findById/", { id }).then((res) => {
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
export const useAdminsFindById = (id) => {
    var form = reactive({});

    canAdminsFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canAdminsInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/admins/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("admins_insert", res.data);
                        event.emit("admins_change", res.data);
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
export const canAdminsUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/admins/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("admins_update", res.data);
                        event.emit("admins_change", res.data);
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
export const canAdminsDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/admins/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("admins_delete", res.data);
                        event.emit("admins_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
