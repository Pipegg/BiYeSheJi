<template>
    <div class="views-kechengxinxi-updt">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加课程信息 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item label="课程编号" prop="kechengbianhao" :rules="[{required:true, message:'请填写课程编号'}]">
                        <el-input type="text" placeholder="输入课程编号" style="width: 450px" v-model="form.kechengbianhao" />
                    </el-form-item>

                    <el-form-item label="课程名称" prop="kechengmingcheng" required :rules="[{required:true, message:'请填写课程名称'}]">
                        <el-input type="text" placeholder="输入课程名称" style="width: 450px" v-model="form.kechengmingcheng" />
                    </el-form-item>

                    <el-form-item label="课程分类" prop="kechengfenlei" required :rules="[{required:true, message:'请填写课程分类'}]">
                        <el-select v-model="form.kechengfenlei"
                            ><e-select-option type="option" module="kechengfenlei" value="id" label="fenleimingcheng"></e-select-option
                        ></el-select>
                    </el-form-item>

                    <el-form-item label="课程封面" prop="kechengfengmian" required :rules="[{required:true, message:'请填写课程封面'}]">
                        <e-upload-image v-model="form.kechengfengmian" is-paste></e-upload-image>
                    </el-form-item>

                    <el-form-item label="课程要点" prop="kechengyaodian" required :rules="[{required:true, message:'请填写课程要点'}]">
                        <el-input type="text" placeholder="输入课程要点" style="width: 450px" v-model="form.kechengyaodian" />
                    </el-form-item>

                    <el-form-item label="发布教师" prop="fabujiaoshi"> <el-input v-model="form.fabujiaoshi" readonly style="width: 250px"></el-input> </el-form-item>

                    <el-form-item label="课程详情" prop="kechengxiangqing">
                        <e-editor v-model="form.kechengxiangqing" @getContent="getkechengxiangqingContent"></e-editor>
                    </el-form-item>

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
    import { useKechengxinxiFindById, canKechengxinxiFindById, canKechengxinxiUpdate } from "@/module";

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
    const form = useKechengxinxiFindById(props.id);
    const emit = defineEmits(["success"]);
    const formModel = ref();
    const loading = ref(false);

    const submit = () => {
        formModel.value.validate().then((res) => {
            if (loading.value) return;
            loading.value = true;
            canKechengxinxiUpdate(form).then(
                (res) => {
                    loading.value = false;
                    if (res.code == 0) {
                        emit("success", res.data);
                        if (props.isHouxu) {
                            ElMessage.success("更新成功");
                            router.go(-1);
                        }
                    } else {
                        ElMessageBox.alert(res.msg);
                    }
                },
                (err) => {
                    loading.value = false;
                    ElMessageBox.alert(err.message);
                }
            );
        });
    };

    const getkechengxiangqingContent = (v) => {
        form.kechengxiangqing = v;
    };
</script>

<style scoped lang="scss">
    .views-kechengxinxi-updt {
    }
</style>
