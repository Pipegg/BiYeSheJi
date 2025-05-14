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

export const XueshengCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        xuehao: "",
        mima: "",
        xingming: "",
        xingbie: "",
        shouji: "",
        youxiang: "",
        shenfenzheng: "",
        touxiang: "",

        issh: "否",
    };

    return form;
};

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canXueshengCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = XueshengCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取学生 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useXueshengCreateForm = () => {
    const form = XueshengCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canXueshengSelect = (filter, result) => {
    http.post("/xuesheng/index/").then((res) => {
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
export const useXueshengSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canXueshengSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canXueshengFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/xuesheng/findById/", { id }).then((res) => {
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
export const useXueshengFindById = (id) => {
    var form = reactive({});

    canXueshengFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canXueshengInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuesheng/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuesheng_insert", res.data);
                        event.emit("xuesheng_change", res.data);
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
export const canXueshengUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuesheng/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuesheng_update", res.data);
                        event.emit("xuesheng_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

export const canXueshengCheckIssh = (row) => {
    return new Promise((resolve, reject) => {
        var id = row.id;
        var value = row.issh === "是" ? "否" : "是";
        http.get("/xuesheng/admin/checkIssh/", { id, value })
            .json()
            .then(
                (res) => {
                    if (res.code == 0) {
                        row.issh = value;
                    }
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuesheng_update", row);
                        event.emit("xuesheng_change", row);
                    }
                },
                (err) => {
                    ElMessageBox.alert(err.message);
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
export const canXueshengDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/xuesheng/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuesheng_delete", res.data);
                        event.emit("xuesheng_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
