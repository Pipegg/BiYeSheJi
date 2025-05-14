<template>
    <div class="views-kechengshipin-detail">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 课程视频详情 </span>
                    </div>
                </template>

                <div id="printdetail">
                    <el-descriptions class="margin-top" :column="3" border>
                        <el-descriptions-item label="课程编号"> {{ map.kechengbianhao }} </el-descriptions-item>
                        <el-descriptions-item label="课程名称"> {{ map.kechengmingcheng }} </el-descriptions-item>
                        <el-descriptions-item label="课程分类">
                            <e-select-view module="kechengfenlei" :value="map.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                        </el-descriptions-item>
                        <el-descriptions-item label="发布教师"> {{ map.fabujiaoshi }} </el-descriptions-item>
                        <el-descriptions-item label="视频名称"> {{ map.shipinmingcheng }} </el-descriptions-item>
                        <el-descriptions-item label="学习次数"> {{ map.xuexicishu }} </el-descriptions-item>
                        <el-descriptions-item label="发布时间"> {{ map.addtime }} </el-descriptions-item>
                    </el-descriptions>

                    <el-descriptions direction="vertical" class="margin-top" :column="1" border>
                        <el-descriptions-item label="视频"> <vue3VideoPlay width="100%" :src="$formatImageSrc(map.shipin)" poster="" /> </el-descriptions-item>
                        <el-descriptions-item label="视频介绍"> <div v-html="map.shipinjieshao"></div> </el-descriptions-item>
                    </el-descriptions>
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
    import "vue3-video-play/dist/style.css";
    import vue3VideoPlay from "vue3-video-play";

    import { ref, reactive, watch, computed } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { extend } from "@/utils/extend";
    import { useKechengshipinFindById, canKechengshipinFindById } from "@/module";

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
    const map = useKechengshipinFindById(props.id);
    // 当url参数id变更时，自动更新map中的数据
    watch(
        () => props.id,
        (id) => {
            canKechengshipinFindById(id).then((res) => {
                extend(map, res);
            });
        }
    );
    // end 获取详情页面的一行数据
</script>

<style scoped lang="scss">
    .views-kechengshipin-detail {
    }
</style>
