<template>
    <div class="views-zuoyepiyue-updt">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加作业批阅 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item v-if="isRead" label="课程编号" prop="kechengbianhao"> {{ form.kechengbianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程名称" prop="kechengmingcheng"> {{ form.kechengmingcheng }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程分类" prop="kechengfenlei">
                        <e-select-view module="kechengfenlei" :value="form.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                    </el-form-item>

                    <el-form-item v-if="isRead" label="发布教师" prop="fabujiaoshi"> {{ form.fabujiaoshi }} </el-form-item>

                    <el-form-item v-if="isRead" label="作业名称" prop="zuoyemingcheng"> {{ form.zuoyemingcheng }} </el-form-item>

                    <el-form-item v-if="isRead" label="作业附件" prop="zuoyefujian"> <e-file-list v-model="form.zuoyefujian"></e-file-list> </el-form-item>

                    <el-form-item v-if="isRead" label="学生姓名" prop="xueshengxingming"> {{ form.xueshengxingming }} </el-form-item>

                    <el-form-item v-if="isRead" label="提交学生" prop="tijiaoxuesheng"> {{ form.tijiaoxuesheng }} </el-form-item>

                    <el-form-item
                        label="分数"
                        prop="fenshu"
                        required
                        :rules="[{required:true, message:'请填写分数'}, {validator:rule.checkNumber, message:'输入一个有效数字'}, {validator:rule.checkMin, value:1}, {validator:rule.checkMax, value:100}]"
                    >
                        <el-input type="number" placeholder="输入分数" style="width: 450px" v-model.number="form.fenshu" />
                    </el-form-item>

                    <el-form-item label="评语" prop="pingyu" required :rules="[{required:true, message:'请填写评语'}]">
                        <el-input type="textarea" v-model="form.pingyu"></el-input>
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

    import { ref, reactive, computed, watch } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { ElMessage, ElMessageBox } from "element-plus";
    import { useZuoyepiyueFindById, canZuoyepiyueFindById, canZuoyepiyueUpdate, canTijiaozuoyeFindById } from "@/module";
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
    const form = useZuoyepiyueFindById(props.id);
    const emit = defineEmits(["success"]);
    const formModel = ref();
    const loading = ref(false);

    const submit = () => {
        formModel.value.validate().then((res) => {
            if (loading.value) return;
            loading.value = true;
            canZuoyepiyueUpdate(form).then(
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
        () => form.tijiaozuoyeid,
        (id) => {
            canTijiaozuoyeFindById(id).then((res) => {
                extend(readMap, res);
            });
        }
    );
</script>

<style scoped lang="scss">
    .views-zuoyepiyue-updt {
    }
</style>
