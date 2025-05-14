<template>
    <div class="views-kechengziyuan-list">
        <div>
            <el-card class="box-card">
                <template #header>
                    <div class="clearfix">
                        <span class="title"> 课程资源查询 </span>
                    </div>
                </template>

                <div class="form-search">
                    <el-form @submit.prevent.stop :inline="true" size="small">
                        <el-form-item label="课程编号">
                            <el-input v-model="search.kechengbianhao"></el-input>
                        </el-form-item>
                        <el-form-item label="课程名称">
                            <el-input v-model="search.kechengmingcheng"></el-input>
                        </el-form-item>
                        <el-form-item label="课程分类">
                            <el-select v-model="search.kechengfenlei"
                                ><el-option label="请选择" value=""></el-option
                                ><e-select-option type="option" module="kechengfenlei" value="id" label="fenleimingcheng"></e-select-option
                            ></el-select>
                        </el-form-item>
                        <el-form-item label="资源名称">
                            <el-input v-model="search.ziyuanmingcheng"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="searchSubmit" icon="el-icon-search">查询</el-button>
                        </el-form-item>
                    </el-form>
                </div>

                <el-table border :data="lists" style="width: 100%" @sort-change="sortChange" highlight-current-row>
                    <el-table-column type="index" label="#"></el-table-column>
                    <!-- 序号 -->

                    <el-table-column prop="kechengbianhao" label="课程编号" width="130">
                        <template #default="{row}"> {{ row.kechengbianhao }} </template>
                    </el-table-column>
                    <el-table-column prop="kechengmingcheng" label="课程名称">
                        <template #default="{row}"> {{ row.kechengmingcheng }} </template>
                    </el-table-column>
                    <el-table-column prop="kechengfenlei" label="课程分类" width="80">
                        <template #default="{row}"> <e-select-view module="kechengfenlei" :value="row.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view> </template>
                    </el-table-column>
                    <el-table-column prop="fabujiaoshi" label="发布教师" width="180">
                        <template #default="{row}"> {{ row.fabujiaoshi }} </template>
                    </el-table-column>
                    <el-table-column prop="ziyuanmingcheng" label="资源名称">
                        <template #default="{row}"> {{ row.ziyuanmingcheng }} </template>
                    </el-table-column>
                    <el-table-column prop="ziyuanfujian" label="资源附件">
                        <template #default="{row}"> <e-file-list v-model="row.ziyuanfujian"></e-file-list> </template>
                    </el-table-column>
                    <el-table-column prop="addtime" label="发布时间">
                        <template #default="{row}"> {{ row.addtime.substring(0,19) }} </template>
                    </el-table-column>

                    <el-table-column label="操作" fixed="right" width="180">
                        <template #default="{row}">
                            <el-button-group>
                                <el-tooltip effect="dark" content="详情" placement="top-start"
                                    ><el-button type="info" :icon="InfoFilled" size="small" @click="$router.push('/admin/kechengziyuan/detail?id='+row.id)">详情</el-button>
                                </el-tooltip>
                                <el-tooltip effect="dark" content="编辑" placement="top-start"
                                    ><el-button type="success" :icon="Edit" size="small" @click="$router.push('/admin/kechengziyuan/updt?id='+row.id)">编辑</el-button>
                                </el-tooltip>
                                <el-tooltip effect="dark" content="删除" placement="top-start"
                                    ><el-button type="danger" :icon="Delete" size="small" @click="deleteItems(row.id)">删除</el-button>
                                </el-tooltip>
                            </el-button-group>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="e-pages" style="margin-top: 10px; text-align: center">
                    <el-pagination
                        @current-change="loadList"
                        :page-sizes="[12, 24, 36, 48,60]"
                        v-model:current-page="search.page"
                        v-model:page-size="search.pagesize"
                        @size-change="sizeChange"
                        layout="total, sizes, prev, pager, next"
                        :total="totalCount"
                    >
                    </el-pagination>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";
    import router from "@/router";

    import { ref, reactive, watch, unref, onBeforeMount } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { canKechengziyuanSelect, useKechengziyuanSelect, canKechengziyuanDelete } from "@/module";
    import { extend } from "@/utils/extend";
    import { ElMessageBox, ElMessage } from "element-plus";
    import { InfoFilled, Edit, Delete } from "@element-plus/icons-vue";

    const route = useRoute();
    const search = reactive({
        kechengxinxiid: "",
        kechengbianhao: "",
        kechengmingcheng: "",
        kechengfenlei: "",
        ziyuanmingcheng: "",
        page: 1, // 当前页
        pagesize: 12, // 每页行数
        orderby: "id", // 排序字段
        sort: "desc", // 排序类型
    });
    extend(search, route.query);
    // 链接参数变化时更新这些内容
    watch(
        () => route.query,
        () => {
            extend(search, route.query);
            loadList(1);
        },
        { deep: true }
    );

    // 总行数
    const totalCount = ref(0);
    // 列表数据
    const lists = ref([]);
    // 加载状态
    const loading = ref(false);

    // 排序操作
    const sortChange = (e) => {
        console.log(e);
        if (e.order == null) {
            search.orderby = "id";
            search.sort = "desc";
        } else {
            search.orderby = e.prop;
            search.sort = e.order == "ascending" ? "asc" : "desc";
        }
        loadList(1);
    };
    // 设置页数多少
    const sizeChange = (e) => {
        search.pagesize = e;
        loadList(1);
    };

    const deleteItems = (ids) => {
        return new Promise((resolve, reject) => {
            ElMessageBox.confirm("确定删除？")
                .then((res) => {
                    canKechengziyuanDelete(ids).then((res) => {
                        if (res.code == 0) {
                            ElMessage.success("删除成功");
                            loadList(search.page);
                            resolve(res.data);
                        } else {
                            ElMessage.error(res.msg);
                        }
                    });
                })
                .catch((err) => {
                    reject(err);
                });
        });
    };

    // 加载课程资源列表方法
    const loadList = (page) => {
        // 加载
        if (unref(loading)) return;
        loading.value = true;
        search.page = page;

        http.post("/kechengziyuan/admin/fabujiaoshi/", search).then(
            (res) => {
                loading.value = false;
                if (res.code == 0) {
                    var data = res.data;
                    lists.value = data.lists.records;
                    totalCount.value = data.lists.total;
                }
            },
            (err) => {
                ElMessage.error(err.message);
            }
        );
    };

    onBeforeMount(() => {
        loadList(1);
    });
    const searchSubmit = () => {
        loadList(1);
    };
</script>

<style scoped lang="scss">
    .views-kechengziyuan-list {
    }
</style>
