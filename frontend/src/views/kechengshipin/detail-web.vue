<template>
    <div class="views-kechengshipin-web-detail">
        <div>
            <e-container>
                <div class="bilibili" style="background: #FFFFFF">
                    <div class="plp-l">
                        <div class="player-module">
                            <div class="stardust-player">
                                <div class="player">
                                    <div class="bilibili-player relative">
                                        <div class="bilibili-player-area">
                                            <div class="bilibili-player-video-wrap">
                                                <vue3VideoPlay width="100%" :src="$formatImageSrc(map.shipin)" poster="" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="plp-r">
                        <div class="media-wrapper" style="color: #535353">
                            <h1 v-text="map.shipinmingcheng"></h1>
                            <div class="tool-bar clearfix">
                                <div class="like-info">
                                    <span>课程编号 : {{ map.kechengbianhao }}</span>
                                </div>
                                <div class="like-info">
                                    <span>课程名称 : {{ map.kechengmingcheng }}</span>
                                </div>
                                <div class="like-info">
                                    <span>课程分类 : <e-select-view module="kechengfenlei" :value="map.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view></span>
                                </div>
                                <div class="like-info">
                                    <span>学习次数 : {{ map.xuexicishu }}</span>
                                </div>
                                <div class="like-info">
                                    <span>发布时间 : {{ map.addtime }}</span>
                                </div>
                            </div>


                        </div>
                    </div>
                </div>
            </e-container>
        </div>
        <div>
            <e-container>
                <div class="title-modelbox-widget">
                    <h3 class="section-title">视频详情</h3>
                    <div class="sidebar-widget-body">
                        <div style="text-indent: 3em">
                            <div v-html="map.shipinjieshao"></div>
                        </div>
                    </div>
                    <!-- /.sidebar-widget-body -->
                </div>
            </e-container>
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
    import { session, substr } from "@/utils/utils";
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
    const loadWebFind = (id) => {
        http.post("/kechengshipin/detail/", { id }).then((res) => {
            console.log(res.data);
        });
    };
    watch(() => props.id, loadWebFind, { immediate: true });
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
    .views-kechengshipin-web-detail {
    }
</style>
