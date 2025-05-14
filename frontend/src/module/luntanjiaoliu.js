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

export const LuntanjiaoliuCreateForm = () => {
    var route = unref(router.currentRoute);
    const userStore = useUserStore();
    const $session = userStore.session;
    if (!route.query) {
        route = useRoute();
    }
    const form = {
        bianhao: rule.getID(),
        biaoti: "",
        fenlei: "",
        tupian: "",
        faburen: $session.username,
        hudongneirong: "",
        quanxian: $session.cx,
        xingming: $session.xingming,
        touxiang: $session.touxiang,

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
export const canLuntanjiaoliuCreateForm = () => {
    return new Promise(async (resolve, reject) => {
        var form = LuntanjiaoliuCreateForm();
        resolve({ form });
    });
};

/**
 * 响应式获取论坛交流 模块的表单字段数据
 * @return {UnwrapNestedRefs<{}>}
 */
export const useLuntanjiaoliuCreateForm = () => {
    const form = LuntanjiaoliuCreateForm();
    const formReactive = reactive(form);

    return { form: formReactive };
};

export const canLuntanjiaoliuSelect = (filter, result) => {
    http.post("/luntanjiaoliu/index/").then((res) => {
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
export const useLuntanjiaoliuSelect = (filter) => {
    const result = reactive({
        lists: [],
        total: {},
    });
    canLuntanjiaoliuSelect(filter, result);
    return result;
};

/**
 * 根据
 * @param id
 * @return {Promise|form}
 */
export const canLuntanjiaoliuFindById = (id) => {
    return new Promise((resolve, reject) => {
        // 读取后台数据
        http.get("/luntanjiaoliu/findById/", { id }).then((res) => {
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
export const useLuntanjiaoliuFindById = (id) => {
    var form = reactive({});

    canLuntanjiaoliuFindById(id).then((res) => {
        extend(form, res);
    });
    return form;
};

/**
 * 根据数据,插入到数据库中
 * @param data
 * @return {Promise<unknown>}
 */
export const canLuntanjiaoliuInsert = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/luntanjiaoliu/insert/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanjiaoliu_insert", res.data);
                        event.emit("luntanjiaoliu_change", res.data);
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
export const canLuntanjiaoliuUpdate = (data) => {
    return new Promise((resolve, reject) => {
        http.post("/luntanjiaoliu/update/", data)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanjiaoliu_update", res.data);
                        event.emit("luntanjiaoliu_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};

export const canLuntanjiaoliuCheckIssh = (row) => {
    return new Promise((resolve, reject) => {
        var id = row.id;
        var value = row.issh === "是" ? "否" : "是";
        http.get("/luntanjiaoliu/admin/checkIssh/", { id, value })
            .json()
            .then(
                (res) => {
                    if (res.code == 0) {
                        row.issh = value;
                    }
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanjiaoliu_update", row);
                        event.emit("luntanjiaoliu_change", row);
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
export const canLuntanjiaoliuDelete = (id) => {
    var res = [];
    if (!isArray(id)) {
        res.push(id);
    } else {
        res = id;
    }

    return new Promise((resolve, reject) => {
        http.post("/luntanjiaoliu/delete/", res)
            .json()
            .then(
                (res) => {
                    resolve(res);
                    if (res.code == 0) {
                        event.emit("luntanjiaoliu_delete", res.data);
                        event.emit("luntanjiaoliu_change", res.data);
                    }
                },
                (err) => {
                    reject(err);
                }
            );
    });
};
