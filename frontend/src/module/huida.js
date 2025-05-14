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

export const HuidaCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        wenti: route.query?.wenda,
        huidaneirong: "",
        quanzhi: "10",
        huidacishu: "",
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canHuidaCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = HuidaCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取回答 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useHuidaCreateForm = () => {
    const form = HuidaCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canHuidaSelect = (filter, result) => {
    http.post("/huida/index/").then((res) => {
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
export const useHuidaSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canHuidaSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canHuidaFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/huida/findById/", { id }).then((res) => {
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
export const useHuidaFindById = (id) => {
    var form = reactive({});

    canHuidaFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canHuidaInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/huida/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("huida_insert", res.data);
                        event.emit("huida_change", res.data);
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
export const canHuidaUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/huida/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("huida_update", res.data);
                        event.emit("huida_change", res.data);
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
export const canHuidaDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/huida/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("huida_delete", res.data);
                        event.emit("huida_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
