<template>
    <table width="100%" class="floot">
        <tbody>
            <tr class="vt">
                <td rowspan="2" class="floot_left">
                    <slot name="user"> </slot>
                </td>
                <td class="floot_right">
                    <a name="post_2920754"></a>
                    <!--印戳-->
                    <!--楼层信息及编辑-->
                    <div class="tipTop s6"><a class="s2 b cp">{{ floor }}</a>&nbsp;<span>发表于: {{ addtime ? addtime.substr(0,10) : '' }}</span></div>
                    <div class="read_h1" v-if="title" style="margin-bottom: 10px">{{ title }}</div>
                    <div class="tpc_content">
                        <div class="" v-if="shipin">
                            <vue3VideoPlay width="100%" :src="$formatImageSrc(shipin)" poster="" />
                        </div>
                        <div class="f14 mb10">
                            <slot>
                                <div v-html="content"></div>
                            </slot>
                        </div>
                    </div>
                    <!--content_read-->
                </td>
            </tr>
            <tr>
                <td class="floot_bottom">
                    <!--评分-->
                    <div id="w_2920754" class="c"></div>
                    <!--评分结束-->
                    <div class="tipBottom cc">
                        <div class="fl">
                            <slot name="bottom-left"></slot>
                        </div>
                        <div class="fr">
                            <slot name="bottom-right"></slot>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</template>
<style type="text/scss" lang="scss">
    .floot_bottom {
        background: #ffffff;
    }
</style>
<script>
    import "vue3-video-play/dist/style.css";
    import vue3VideoPlay from "vue3-video-play";
    export default {
        name: "e-forum-item",
        data() {
            return {};
        },
        components: { vue3VideoPlay },
        props: {
            title: {
                type: String,
            },
            content: {
                type: String,
                required: true,
            },
            shipin: {
                type: String,
            },
            addtime: {
                type: String,
            },
            floor: [Number, String],
        },
        watch: {},
        computed: {},
        methods: {},
        created() {},
        mounted() {},
        destroyed() {},
    };
</script>
