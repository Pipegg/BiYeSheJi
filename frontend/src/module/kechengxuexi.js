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

export const KechengxuexiCreateForm = () => {
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
        xuexibianhao: rule.getID(),
        xueshengyonghu: $session.username,
        xuexizhuangtai: "待学习",
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
export const canKechengxuexiCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = KechengxuexiCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canKechengxinxiFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.kechengxinxiid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取课程学习 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useKechengxuexiCreateForm = (id) => {
    const form = KechengxuexiCreateForm();
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

export const canKechengxuexiSelect = (filter, result) => {
    http.post("/kechengxuexi/index/").then((res) => {
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
export const useKechengxuexiSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canKechengxuexiSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canKechengxuexiFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/kechengxuexi/findById/", { id }).then((res) => {
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
export const useKechengxuexiFindById = (id) => {
    var form = reactive({});

    canKechengxuexiFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canKechengxuexiInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengxuexi/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxuexi_insert", res.data);
                        event.emit("kechengxuexi_change", res.data);
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
export const canKechengxuexiUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/kechengxuexi/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxuexi_update", res.data);
                        event.emit("kechengxuexi_change", res.data);
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
export const canKechengxuexiDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/kechengxuexi/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("kechengxuexi_delete", res.data);
                        event.emit("kechengxuexi_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
