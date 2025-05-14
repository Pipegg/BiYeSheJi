import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canKechengshipinFindById } from "./kechengshipin";

/**
 * 响应式的对象数据
 */

export const XuexijiluCreateForm = () => {
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
        fabujiaoshi: $session.username,
        shipinmingcheng: "",
        xueshengyonghu: $session.username,
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["kechengshipinid", "kechengbianhao", "kechengmingcheng", "kechengfenlei", "fabujiaoshi", "shipinmingcheng"];
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
export const canXuexijiluCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = XuexijiluCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canKechengshipinFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.kechengshipinid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取学习记录 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useXuexijiluCreateForm = (id) => {
    const form = XuexijiluCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canKechengshipinFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.kechengshipinid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canXuexijiluSelect = (filter, result) => {
    http.post("/xuexijilu/index/").then((res) => {
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
export const useXuexijiluSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canXuexijiluSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canXuexijiluFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/xuexijilu/findById/", { id }).then((res) => {
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
export const useXuexijiluFindById = (id) => {
    var form = reactive({});

    canXuexijiluFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canXuexijiluInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuexijilu/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijilu_insert", res.data);
                        event.emit("xuexijilu_change", res.data);
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
export const canXuexijiluUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/xuexijilu/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijilu_update", res.data);
                        event.emit("xuexijilu_change", res.data);
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
export const canXuexijiluDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/xuexijilu/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("xuexijilu_delete", res.data);
                        event.emit("xuexijilu_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
