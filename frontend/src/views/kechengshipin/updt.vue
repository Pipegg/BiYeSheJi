<template>
    <div class="views-kechengshipin-updt">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 添加课程视频 </span>
                    </div>
                </template>

                <el-form :model="form" ref="formModel" :label-width="labelWidth" status-icon validate-on-rule-change>
                    <el-form-item v-if="isRead" label="课程编号" prop="kechengbianhao"> {{ form.kechengbianhao }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程名称" prop="kechengmingcheng"> {{ form.kechengmingcheng }} </el-form-item>

                    <el-form-item v-if="isRead" label="课程分类" prop="kechengfenlei">
                        <e-select-view module="kechengfenlei" :value="form.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                    </el-form-item>

                    <el-form-item v-if="isRead" label="发布教师" prop="fabujiaoshi"> {{ form.fabujiaoshi }} </el-form-item>

                    <el-form-item label="视频名称" prop="shipinmingcheng" required :rules="[{required:true, message:'请填写视频名称'}]">
                        <el-input type="text" placeholder="输入视频名称" style="width: 450px" v-model="form.shipinmingcheng" />
                    </el-form-item>

                    <el-form-item label="视频" prop="shipin" required :rules="[{required:true, message:'请填写视频'}]">
                        <e-upload-file v-model="form.shipin"></e-upload-file>
                    </el-form-item>

                    <el-form-item label="视频介绍" prop="shipinjieshao"> <e-editor v-model="form.shipinjieshao" @getContent="getshipinjieshaoContent"></e-editor> </el-form-item>

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

    import { ref, reactive, computed, watch } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { ElMessage, ElMessageBox } from "element-plus";
    import { useKechengshipinFindById, canKechengshipinFindById, canKechengshipinUpdate, canKechengxinxiFindById } from "@/module";
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
    const form = useKechengshipinFindById(props.id);
    const emit = defineEmits(["success"]);
    const formModel = ref();
    const loading = ref(false);

    const submit = () => {
        formModel.value.validate().then((res) => {
            if (loading.value) return;
            loading.value = true;
            canKechengshipinUpdate(form).then(
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
        () => form.kechengxinxiid,
        (id) => {
            canKechengxinxiFindById(id).then((res) => {
                extend(readMap, res);
            });
        }
    );
    const getshipinjieshaoContent = (v) => {
        form.shipinjieshao = v;
    };
</script>

<style scoped lang="scss">
    .views-kechengshipin-updt {
    }
</style>
