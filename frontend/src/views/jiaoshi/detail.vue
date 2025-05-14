<template>
    <div class="views-jiaoshi-detail">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 教师详情 </span>
                    </div>
                </template>

                <div id="printdetail">
                    <el-descriptions class="margin-top" :column="3" border>
                        <el-descriptions-item label="工号"> {{ map.gonghao }} </el-descriptions-item>
                        <el-descriptions-item label="密码"> {{ map.mima }} </el-descriptions-item>
                        <el-descriptions-item label="姓名"> {{ map.xingming }} </el-descriptions-item>
                        <el-descriptions-item label="性别"> {{ map.xingbie }} </el-descriptions-item>
                        <el-descriptions-item label="职称"> {{ map.zhicheng }} </el-descriptions-item>
                        <el-descriptions-item label="联系方式"> {{ map.lianxifangshi }} </el-descriptions-item>
                        <el-descriptions-item label="邮箱"> {{ map.youxiang }} </el-descriptions-item>
                        <el-descriptions-item label="头像"> <e-img :src="map.touxiang" class="detail-image" style="max-width: 120px" /> </el-descriptions-item>
                    </el-descriptions>

                    <el-descriptions direction="vertical" class="margin-top" :column="1" border> </el-descriptions>
                </div>
                <div class="no-print" v-if="isShowBtn">
                    <el-button @click="$router.go(-1)">返回</el-button>
                    <el-button @click="$print('#printdetail')">打印</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";

    import { ref, reactive, watch, computed } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { extend } from "@/utils/extend";
    import { useJiaoshiFindById, canJiaoshiFindById } from "@/module";

    const route = useRoute();
    const props = defineProps({
        id: {
            type: [Number, String],
        },
        isShowBtn: {
            type: Boolean,
            default: true,
        },
    });

    // 获取详情页面的一行数据,当url参数id变更时，自动
    const map = useJiaoshiFindById(props.id);
    // 当url参数id变更时，自动更新map中的数据
    watch(
        () => props.id,
        (id) => {
            canJiaoshiFindById(id).then((res) => {
                extend(map, res);
            });
        }
    );
    // end 获取详情页面的一行数据
</script>

<style scoped lang="scss">
    .views-jiaoshi-detail {
    }
</style>
