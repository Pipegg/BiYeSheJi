<template>
    <div class="views-luntanjiaoliu-web-detail">
        <div>
            <e-container>
                <div class="title-sn-title1">
                    <div class="sn-title">
                        <span> 详情 </span>
                    </div>
                    <div class="sn-content">
                        <e-forum>
                            <e-forum-item floor="楼主" :addtime="map.biaoti" :content="map.hudongneirong">
                                <template #user>
                                    <e-user :nickname="map.xingming" :headimg="map.touxiang">

                                    </e-user>
                                </template>
                            </e-forum-item>
                            <e-forum-page :lists="replyList">
                                <template v-slot:default="{row,floor}">
                                    <e-forum-item :floor="floor" :addtime="row.addtime" :content="row.jiaoliuneirong">
                                        <template #user>
                                            <e-user :nickname="row.xingming" :headimg="row.touxiang">

                                            </e-user>
                                        </template>
                                        <template #bottom-right>
                                            <div>
                                                <el-button type="success" @click="onSetReplyContent(floor,row.xingming,row.jiaoliuneirong)">回复</el-button>
                                            </div>
                                        </template>
                                    </e-forum-item>
                                </template>
                            </e-forum-page>
                            <e-forum-item floor="回复" v-if="$session.username">
                                <template #user>
                                    <e-user :nickname="$session.xingming" :headimg="$session.touxiang">
                                        <dl class="cc">
                                            <dt>学号</dt>
                                            <dd>{{ $session.xuehao }}</dd>
                                        </dl>
                                        <dl class="cc">
                                            <dt>性别</dt>
                                            <dd>{{ $session.xingbie }}</dd>
                                        </dl>
                                    </e-user>
                                </template>
                                <e-editor v-model="replyContent" @getContent="getReplyContent"></e-editor>
                                <el-button type="success" @click="onReplyClick">回复</el-button>
                            </e-forum-item>
                        </e-forum>
                    </div>
                </div>
            </e-container>
        </div>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";
    import EForum from "@/components/forum/forum.vue";
    import EForumItem from "@/components/forum/item.vue";
    import EForumPage from "@/components/forum/forum-page.vue";
    import EUser from "@/components/forum/user.vue";
    import EEditor from "@/components/EEditor.vue";

    import { ref, reactive, watch, computed, unref } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { extend } from "@/utils/extend";
    import { useLuntanjiaoliuFindById, canLuntanjiaoliuFindById, canJiaoliuhuifuInsert, canJiaoliuhuifuCreateForm } from "@/module";
    import { ElMessage } from "element-plus";

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
    const map = useLuntanjiaoliuFindById(props.id);
    // 当url参数id变更时，自动更新map中的数据
    watch(
        () => props.id,
        (id) => {
            canLuntanjiaoliuFindById(id).then((res) => {
                extend(map, res);
            });
        }
    );
    // end 获取详情页面的一行数据

    const replyContent = ref("");
    const getReplyContent = (v) => {
        replyContent.value = v;
    };
    const onReplyClick = async () => {
        const { form, readMap } = await canJiaoliuhuifuCreateForm(route.query.id, map);
        form.jiaoliuneirong = unref(replyContent);

        var res = await canJiaoliuhuifuInsert(form).catch(console.error);
        if (res.code == 0) {
            ElMessage.success("回复成功");
            replyContent.value = `<p>&nbsp;</p>`;
            loadreplyListList(map);
        }
    };
    const onSetReplyContent = (foor, user, content) => {
        replyContent.value = `<blockquote><p>回【${foor}】楼，（${user} 的帖子）</p>${content}</blockquote><p>&nbsp;</p>`;
        window.scrollTo(0, 9999);
    };

    // 获取用户信息
    const user = ref({});
    watch(
        () => map.faburen,
        async (newValue) => {
            user.value = await DB.name("xuesheng").where("xuehao", newValue).find();
        }
    );
    // end 获取用户信息

    // 获取回复列表
    const replyList = ref([]);
    const loadreplyListList = async (map) => {
        replyList.value = await DB.name("jiaoliuhuifu")
            .alias("r")
            .field("r.*")
            .where("r.luntanjiaoliuid", map.id)
            .order("r.id desc")
            .select();
    };
    watch(
        () => map,
        async (newValue) => {
            loadreplyListList(newValue);
        },
        { deep: true }
    );
    // end 获取回复列表
</script>

<style scoped lang="scss">
    .views-luntanjiaoliu-web-detail {
    }
</style>
