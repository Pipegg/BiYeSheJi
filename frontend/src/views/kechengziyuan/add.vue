<template>
    <div class="views-kechengziyuan-add">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加课程资源 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item v-if="isRead" label="课程编号" prop="kechengbianhao"> {{ form.kechengbianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程名称" prop="kechengmingcheng"> {{ form.kechengmingcheng }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程分类" prop="kechengfenlei">
                        <e-select-view module="kechengfenlei" :value="form.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                    </el-form-item>

                    <el-form-item v-if="isRead" label="发布教师" prop="fabujiaoshi"> {{ form.fabujiaoshi }} </el-form-item>

                    <el-form-item label="资源名称" prop="ziyuanmingcheng" required :rules="[{required:true, message:'请填写资源名称'}]">
                        <el-input type="text" placeholder="输入资源名称" style="width: 450px" v-model="form.ziyuanmingcheng" />
                    </el-form-item>

                    <el-form-item label="资源附件" prop="ziyuanfujian" required :rules="[{required:true, message:'请填写资源附件'}]">
                        <e-upload-file v-model="form.ziyuanfujian"></e-upload-file>
                    </el-form-item>

                    <el-form-item label="资源说明" prop="ziyuanshuoming"> <e-editor v-model="form.ziyuanshuoming" @getContent="getziyuanshuomingContent"></e-editor> </el-form-item>

                    <el-form-item v-if="btnText">
                        <el-button type="primary" @click="submit">{{ btnText }}</el-button>
                    </el-form-item>
                </el-form></el-card
            >
        </div>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";
    import rule from "@/utils/rule";
    import router from "@/router";
    import EEditor from "@/components/EEditor.vue";

    import { ref, reactive, computed } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { ElMessage, ElMessageBox } from "element-plus";
    import { useKechengziyuanCreateForm, canKechengziyuanInsert } from "@/module";

    const route = useRoute();
    const props = defineProps({
        id: [String, Number],
        btnText: {
            type: String,
            default: "保存",
        },
        isRead: {
            type: Boolean,
            default: true,
        },
        isHouxu: {
            type: Boolean,
            default: true,
        },
        labelWidth: {
            type: String,
            default: "140px",
        },
    });
    const { form, readMap } = useKechengziyuanCreateForm(props.id);
    const emit = defineEmits(["success"]);
    const formModel = ref();
    const loading = ref(false);
    var submit = () => {
        return new Promise((resolve, reject) => {
            formModel.value
                .validate()
                .then((res) => {
                    if (loading.value) return;
                    loading.value = true;
                    canKechengziyuanInsert(form).then(
                        (res) => {
                            loading.value = false;
                            if (res.code == 0) {
                                emit("success", res.data);
                                if (props.isHouxu) {
                                    ElMessage.success("添加成功");
                                    router.go(-1);
                                }
                            } else {
                                ElMessageBox.alert(res.msg);
                            }
                            resolve(res);
                        },
                        (err) => {
                            loading.value = false;
                            ElMessageBox.alert(err.message);
                            reject(err);
                        }
                    );
                })
                .catch((err) => {
                    reject(err);
                });
        });
    };

    const getziyuanshuomingContent = (v) => {
        form.ziyuanshuoming = v;
    };
</script>

<style scoped lang="scss">
    .views-kechengziyuan-add {
    }
</style>
