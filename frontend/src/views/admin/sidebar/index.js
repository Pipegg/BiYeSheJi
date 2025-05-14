import { useUserStore } from "@/stores/user";

import guanliyuan from "./guanliyuan";
import xuesheng from "./xuesheng";
import jiaoshi from "./jiaoshi";

export function getMenus() {
    return new Promise((resolve, reject) => {
        var userStore = useUserStore();
        var cx = userStore.getSession("cx");
        if (cx == "管理员") {
            resolve(guanliyuan);
        }
        if (cx == "学生") {
            resolve(xuesheng);
        }
        if (cx == "教师") {
            resolve(jiaoshi);
        }
    });
}

export default {
    getMenus,
};
