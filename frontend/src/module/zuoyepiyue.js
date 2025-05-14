import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canTijiaozuoyeFindById } from "./tijiaozuoye";

/**
 * 响应式的对象数据
 */

export const ZuoyepiyueCreateForm = () => {
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
        zuoyemingcheng: "",
        zuoyefujian: "",
        xueshengxingming: $session.xingming,
        tijiaoxuesheng: $session.username,
        fenshu: "",
        pingyu: "",
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["tijiaozuoyeid", "kechengbianhao", "kechengmingcheng", "kechengfenlei", "fabujiaoshi", "zuoyemingcheng", "zuoyefujian", "xueshengxingming", "tijiaoxuesheng"];
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
export const canZuoyepiyueCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = ZuoyepiyueCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canTijiaozuoyeFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.tijiaozuoyeid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取作业批阅 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useZuoyepiyueCreateForm = (id) => {
    const form = ZuoyepiyueCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canTijiaozuoyeFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.tijiaozuoyeid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canZuoyepiyueSelect = (filter, result) => {
    http.post("/zuoyepiyue/index/").then((res) => {
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
export const useZuoyepiyueSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canZuoyepiyueSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canZuoyepiyueFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/zuoyepiyue/findById/", { id }).then((res) => {
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
export const useZuoyepiyueFindById = (id) => {
    var form = reactive({});

    canZuoyepiyueFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canZuoyepiyueInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/zuoyepiyue/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("zuoyepiyue_insert", res.data);
                        event.emit("zuoyepiyue_change", res.data);
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
export const canZuoyepiyueUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/zuoyepiyue/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("zuoyepiyue_update", res.data);
                        event.emit("zuoyepiyue_change", res.data);
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
export const canZuoyepiyueDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/zuoyepiyue/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("zuoyepiyue_delete", res.data);
                        event.emit("zuoyepiyue_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
