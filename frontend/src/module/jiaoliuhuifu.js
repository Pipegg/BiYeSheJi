import http from "@/utils/ajax/http";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores";
import { reactive, ref, unref } from "vue";
import rule from "@/utils/rule";
import { extend, isArray } from "@/utils/extend";
import { ElMessageBox } from "element-plus";
import router from "@/router";
import event from "@/utils/event";

import { canLuntanjiaoliuFindById } from "./luntanjiaoliu";

/**
 * 响应式的对象数据
 */

export const JiaoliuhuifuCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        bianhao: "",
        biaoti: "",
        fenlei: "",
        faburen: $session.username,
        jiaoliuneirong: "",
        huifuren: $session.username,
        huifuquanxian: $session.cx,
        touxiang: $session.touxiang,
        xingming: $session.xingming,
    };

    return form;
};

function exportForm(form, readMap) {
    var autoText = ["luntanjiaoliuid", "bianhao", "biaoti", "fenlei", "faburen"];
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
export const canJiaoliuhuifuCreateForm = (id, readMap) => {
    return new Promise(async (resolve, reject) => {
        var form = JiaoliuhuifuCreateForm();
        if (!readMap || !readMap.id) {
            readMap = await canLuntanjiaoliuFindById(id).catch(reject);
        }
        exportForm(form, readMap);
        form.luntanjiaoliuid = readMap.id;
        resolve({ form, readMap });
    });
};

/**
 * 响应式获取交流回复 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useJiaoliuhuifuCreateForm = (id) => {
    const form = JiaoliuhuifuCreateForm();
    const formReactive = reactive(form);

    const readMap = reactive({});
    canLuntanjiaoliuFindById(id).then(
        (map) => {
            exportForm(formReactive, map);
            extend(readMap, map);
            formReactive.luntanjiaoliuid = map.id;
        },
        (err) => {
            ElMessageBox.alert(err.message);
        }
    );
    return { form: formReactive, readMap };
};

export const canJiaoliuhuifuSelect = (filter, result) => {
    http.post("/jiaoliuhuifu/index/").then((res) => {
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
export const useJiaoliuhuifuSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canJiaoliuhuifuSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canJiaoliuhuifuFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/jiaoliuhuifu/findById/", { id }).then((res) => {
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
export const useJiaoliuhuifuFindById = (id) => {
    var form = reactive({});

    canJiaoliuhuifuFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canJiaoliuhuifuInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/jiaoliuhuifu/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoliuhuifu_insert", res.data);
                        event.emit("jiaoliuhuifu_change", res.data);
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
export const canJiaoliuhuifuUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/jiaoliuhuifu/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoliuhuifu_update", res.data);
                        event.emit("jiaoliuhuifu_change", res.data);
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
export const canJiaoliuhuifuDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/jiaoliuhuifu/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("jiaoliuhuifu_delete", res.data);
                        event.emit("jiaoliuhuifu_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
