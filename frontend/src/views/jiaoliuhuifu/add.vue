<template>
    <div class="views-jiaoliuhuifu-add">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加交流回复 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item v-if="isRead" label="编号" prop="bianhao"> {{ form.bianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="标题" prop="biaoti"> {{ form.biaoti }} </el-form-item>

                    <el-form-item v-if="isRead" label="分类" prop="fenlei">
                        <e-select-view module="luntanfenlei" :value="form.fenlei" select="id" show="fenleimingcheng"></e-select-view>
                    </el-form-item>

                    <el-form-item v-if="isRead" label="发布人" prop="faburen"> {{ form.faburen }} </el-form-item>

                    <el-form-item label="交流内容" prop="jiaoliuneirong" required :rules="[{required:true, message:'请填写交流内容'}]">
                        <e-editor v-model="form.jiaoliuneirong" @getContent="getjiaoliuneirongContent"></e-editor>
                    </el-form-item>

                    <el-form-item label="回复人" prop="huifuren"> <el-input v-model="form.huifuren" readonly style="width: 250px"></el-input> </el-form-item>

                    <el-form-item label="回复权限" prop="huifuquanxian">
                        <el-input type="text" placeholder="输入回复权限" style="width: 450px" v-model="form.huifuquanxian" />
                    </el-form-item>

                    <el-form-item label="头像" prop="touxiang"> <e-upload-image v-model="form.touxiang" is-paste></e-upload-image> </el-form-item>

                    <el-form-item label="姓名" prop="xingming"> <el-input type="text" placeholder="输入姓名" style="width: 450px" v-model="form.xingming" /> </el-form-item>

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
    import { useJiaoliuhuifuCreateForm, canJiaoliuhuifuInsert } from "@/module";

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
    const { form, readMap } = useJiaoliuhuifuCreateForm(props.id);
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
                    canJiaoliuhuifuInsert(form).then(
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

    const getjiaoliuneirongContent = (v) => {
        form.jiaoliuneirong = v;
    };
</script>

<style scoped lang="scss">
    .views-jiaoliuhuifu-add {
    }
</style>
