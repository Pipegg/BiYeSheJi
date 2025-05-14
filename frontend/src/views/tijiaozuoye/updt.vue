<template>
    <div class="views-tijiaozuoye-updt">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加提交作业 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item v-if="isRead" label="课程编号" prop="kechengbianhao"> {{ form.kechengbianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程名称" prop="kechengmingcheng"> {{ form.kechengmingcheng }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程分类" prop="kechengfenlei">
                        <e-select-view module="kechengfenlei" :value="form.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                    </el-form-item>

                    <el-form-item v-if="isRead" label="发布教师" prop="fabujiaoshi"> {{ form.fabujiaoshi }} </el-form-item>

                    <el-form-item v-if="isRead" label="作业编号" prop="zuoyebianhao"> {{ form.zuoyebianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="作业名称" prop="zuoyemingcheng"> {{ form.zuoyemingcheng }} </el-form-item>

                    <el-form-item label="作业附件" prop="zuoyefujian" required :rules="[{required:true, message:'请填写作业附件'}]">
                        <e-upload-file v-model="form.zuoyefujian"></e-upload-file>
                    </el-form-item>

                    <el-form-item label="学生姓名" prop="xueshengxingming">
                        <el-input type="text" placeholder="输入学生姓名" style="width: 450px" v-model="form.xueshengxingming" />
                    </el-form-item>

                    <el-form-item label="提交学生" prop="tijiaoxuesheng"> <el-input v-model="form.tijiaoxuesheng" readonly style="width: 250px"></el-input> </el-form-item>

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

    import { ref, reactive, computed, watch } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { ElMessage, ElMessageBox } from "element-plus";
    import { useTijiaozuoyeFindById, canTijiaozuoyeFindById, canTijiaozuoyeUpdate, canBuzhizuoyeFindById } from "@/module";
    import { extend } from "@/utils/extend";

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
    const form = useTijiaozuoyeFindById(props.id);
    const emit = defineEmits(["success"]);
    const formModel = ref();
    const loading = ref(false);

    const submit = () => {
        formModel.value.validate().then((res) => {
            if (loading.value) return;
            loading.value = true;
            canTijiaozuoyeUpdate(form).then(
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

    const readMap = reactive({});
    watch(
        () => form.buzhizuoyeid,
        (id) => {
            canBuzhizuoyeFindById(id).then((res) => {
                extend(readMap, res);
            });
        }
    );
</script>

<style scoped lang="scss">
    .views-tijiaozuoye-updt {
    }
</style>
