import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canKechengxuexiFindById } from "./kechengxuexi";

/**
 * 响应式的对象数据
 */

export const XuexijinduCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        kechengbianhao: "",
        kechengmingcheng: "",
        kechengfenlei: "",
        xuexibianhao: "",
        fabujiaoshi: $session.username,
        xueshengyonghu: $session.username,
        xuexijindu: "",
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["kechengxuexiid", "kechengbianhao", "kechengmingcheng", "kechengfenlei", "xuexibianhao", "fabujiaoshi", "xueshengyonghu"];
    for (var txt of autoText) {
        form[txt] = readMap[txt];
    }
}

/**
 * 异步模式获取数据
 * @param id
 * @param readMap
 * @return {Promise}
 */
export const canXuexijinduCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = XuexijinduCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canKechengxuexiFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.kechengxuexiid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取学习进度 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useXuexijinduCreateForm = (id) => {
    const form = XuexijinduCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canKechengxuexiFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.kechengxuexiid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canXuexijinduSelect = (filter, result) => {
    http.post("/xuexijindu/index/").then((res) => {
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
export const useXuexijinduSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canXuexijinduSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canXuexijinduFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/xuexijindu/findById/", { id }).then((res) => {
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
export const useXuexijinduFindById = (id) => {
    var form = reactive({});

    canXuexijinduFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canXuexijinduInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuexijindu/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijindu_insert", res.data);
                        event.emit("xuexijindu_change", res.data);
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
export const canXuexijinduUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuexijindu/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijindu_update", res.data);
                        event.emit("xuexijindu_change", res.data);
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
export const canXuexijinduDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/xuexijindu/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijindu_delete", res.data);
                        event.emit("xuexijindu_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
