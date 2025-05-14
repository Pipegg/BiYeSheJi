import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canKechengxinxiFindById } from "./kechengxinxi";

/**
 * 响应式的对象数据
 */

export const KechengshipinCreateForm = () => {
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
        shipin: "",
        shipinjieshao: "",
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["kechengxinxiid", "kechengbianhao", "kechengmingcheng", "kechengfenlei", "fabujiaoshi"];
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
export const canKechengshipinCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = KechengshipinCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canKechengxinxiFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.kechengxinxiid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取课程视频 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useKechengshipinCreateForm = (id) => {
    const form = KechengshipinCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canKechengxinxiFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.kechengxinxiid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canKechengshipinSelect = (filter, result) => {
    http.post("/kechengshipin/index/").then((res) => {
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
export const useKechengshipinSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canKechengshipinSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canKechengshipinFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/kechengshipin/findById/", { id }).then((res) => {
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
export const useKechengshipinFindById = (id) => {
    var form = reactive({});

    canKechengshipinFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canKechengshipinInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengshipin/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengshipin_insert", res.data);
                        event.emit("kechengshipin_change", res.data);
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
export const canKechengshipinUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengshipin/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengshipin_update", res.data);
                        event.emit("kechengshipin_change", res.data);
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
export const canKechengshipinDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/kechengshipin/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengshipin_delete", res.data);
                        event.emit("kechengshipin_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
