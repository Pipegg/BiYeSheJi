<template>
    <div class="views-kechengxinxi-index">
        <div>
            <e-container>
                <div class="title-modelbox-widget1">
                    <h3 class="section-title">课程列表</h3>
                    <div class="sidebar-widget-body">
                        <form action="javascript:;" @submit="searchSubmit" class="form-search">
                            <table class="jd-search">
                                <tbody>
                                    <tr>
                                        <td class="label">课程分类</td>
                                        <td>
                                            <p class="search-radio">
                                                <a href="javascript:;" @click="selectRadio('kechengfenlei','')" :class="{active:!search.kechengfenlei}">全部</a>
                                                <a
                                                    href="javascript:;"
                                                    v-for="r in mapkechengfenlei2"
                                                    @click="selectRadio('kechengfenlei',r.id)"
                                                    :class="{active:search.kechengfenlei == r.id}"
                                                    v-text="r.fenleimingcheng"
                                                >
                                                </a>
                                            </p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="label">课程名称</td>
                                        <td>
                                            <el-input type="text" style="width: 150px" v-model="search.kechengmingcheng" placeholder="请输入关键词"> </el-input>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="label">排序</td>
                                        <td>
                                            <div style="display: flex; justify-content: space-between">
                                                <p class="search-radio">
                                                    <a href="javascript:;" @click="selectRadio('orderby','id')" :class="{active:search.orderby=='id'}">发布时间</a>
                                                </p>
                                                <p class="search-radio">
                                                    <a href="javascript:;" @click="selectRadio('sort','desc')" :class="{active:search.sort=='desc'}">倒序</a>
                                                    <a href="javascript:;" @click="selectRadio('sort','asc')" :class="{active:search.sort=='asc'}">升序</a>
                                                </p>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td></td>
                                        <td>
                                            <el-button type="success" @click="searchSubmit">搜索</el-button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </form>

                        <el-row :gutter="30">
                            <el-col v-for="r in lists" :md="6" :key="r.id" style="margin-bottom: 20px">
                                <article class="single_product v-module-xiezi">
                                    <figure>
                                        <div class="product_thumb" @click="$goto('/kechengxinxi/detail?id='+r.id)">
                                            <div class="label_product"></div>
                                            <e-img class="primary_img" :src="r.kechengfengmian" pb="100" :is-scale="true" />
                                        </div>
                                        <figcaption class="product_content">
                                            <h4 class="product_name"><a href="javascript:;" @click="$goto('/kechengxinxi/detail?id='+r.id)"> {{ r.kechengmingcheng }}</a></h4>
                                            <div class="add_to_cart">
                                                <a href="javascript:;" title="查看详情" @click="$goto('/kechengxinxi/detail?id='+r.id)">查看详情</a>
                                            </div>
                                        </figcaption>
                                    </figure>
                                </article>
                            </el-col>
                        </el-row>

                        <div style="margin-top: 10px; text-align: center">
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
    import router from "@/router";

    import { ref, reactive, watch, unref, onBeforeMount } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { canKechengxinxiSelect, useKechengxinxiSelect, canKechengxinxiDelete } from "@/module";
    import { extend } from "@/utils/extend";
    import { ElMessageBox, ElMessage } from "element-plus";

    const route = useRoute();
    const search = reactive({
        issh: "是",
        kechengbianhao: "",
        kechengmingcheng: "",
        kechengfenlei: "",
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

    // 加载课程信息列表方法
    const loadList = (page) => {
        // 加载
        if (unref(loading)) return;
        loading.value = true;
        search.page = page;

        http.post("/kechengxinxi/index/", search).then(
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
    const selectRadio = (target, name) => {
        search[target] = name;
        searchSubmit(1);
    };

    const searchSubmit = (page = 1) => {
        loadList(1);
    };
    const mapkechengfenlei2 = DB.name("kechengfenlei").field("id,fenleimingcheng").order("id desc").selectRef();
</script>

<style scoped lang="scss">
    .views-kechengxinxi-index {
    }
</style>
