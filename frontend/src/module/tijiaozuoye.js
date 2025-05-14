import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canBuzhizuoyeFindById } from "./buzhizuoye";

/**
 * 响应式的对象数据
 */

export const TijiaozuoyeCreateForm = () => {
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
        zuoyebianhao: "",
        zuoyemingcheng: "",
        zuoyefujian: "",
        xueshengxingming: $session.xingming,
        zuoyezhuangtai: "已提交",
        tijiaoxuesheng: $session.username,
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["buzhizuoyeid", "kechengbianhao", "kechengmingcheng", "kechengfenlei", "fabujiaoshi", "zuoyebianhao", "zuoyemingcheng"];
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
export const canTijiaozuoyeCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = TijiaozuoyeCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canBuzhizuoyeFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.buzhizuoyeid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取提交作业 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useTijiaozuoyeCreateForm = (id) => {
    const form = TijiaozuoyeCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canBuzhizuoyeFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.buzhizuoyeid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canTijiaozuoyeSelect = (filter, result) => {
    http.post("/tijiaozuoye/index/").then((res) => {
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
export const useTijiaozuoyeSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canTijiaozuoyeSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canTijiaozuoyeFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/tijiaozuoye/findById/", { id }).then((res) => {
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
export const useTijiaozuoyeFindById = (id) => {
    var form = reactive({});

    canTijiaozuoyeFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canTijiaozuoyeInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/tijiaozuoye/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("tijiaozuoye_insert", res.data);
                        event.emit("tijiaozuoye_change", res.data);
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
export const canTijiaozuoyeUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/tijiaozuoye/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("tijiaozuoye_update", res.data);
                        event.emit("tijiaozuoye_change", res.data);
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
export const canTijiaozuoyeDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/tijiaozuoye/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("tijiaozuoye_delete", res.data);
                        event.emit("tijiaozuoye_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
