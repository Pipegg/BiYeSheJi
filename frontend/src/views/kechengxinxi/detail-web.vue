<template>
    <div class="views-kechengxinxi-web-detail">
        <!-- Loading state -->
        <e-container v-if="map.loading">
            <div class="loading-container">
                <el-skeleton :rows="10" animated />
                <div class="loading-text">加载课程信息中...</div>
            </div>
        </e-container>
        
        <!-- Error state -->
        <e-container v-else-if="map.error">
            <div class="error-container">
                <el-result
                    icon="error"
                    title="加载失败"
                    :sub-title="map.error"
                >
                    <template #extra>
                        <el-button type="primary" @click="retryLoading">重试加载</el-button>
                        <el-button @click="$router.push('/kechengxinxi/list')">返回列表</el-button>
                    </template>
                </el-result>
            </div>
        </e-container>
        
        <!-- Cache notification -->
        <el-alert
            v-if="map.fromCache"
            title="您正在查看缓存的数据，可能不是最新内容"
            type="warning"
            :closable="false"
            show-icon
            style="margin-bottom: 15px;"
        />
        
        <!-- Mock data notification -->
        <el-alert
            v-if="map.isMockData"
            title="由于网络问题，当前显示的是临时数据，请稍后刷新"
            type="error"
            :closable="false"
            show-icon
            style="margin-bottom: 15px;"
        />
        
        <!-- Content state - Only show when not loading and no error -->
        <div v-if="!map.loading && !map.error">
            <e-container>
                <div class="title-modelbox-widget">
                    <h3 class="section-title">课程详情</h3>
                    <div class="sidebar-widget-body">
                        <div class="">
                            <div class="goods-info clearfix">
                                <div class="gallery-list">
                                    <e-shangpinban :images="map.kechengfengmian"></e-shangpinban>
                                </div>
                                <div class="goods-right-content">
                                    <h3 class="title" v-text="map.kechengmingcheng"></h3>
                                    <div class="descount">
                                        <div>
                                            <span class="name"> 课程编号： </span>
                                            <span class="val"> {{ map.kechengbianhao }} </span>
                                        </div>
                                        <div>
                                            <span class="name"> 课程分类： </span>
                                            <span class="val">
                                                <e-select-view module="kechengfenlei" :value="map.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                                            </span>
                                        </div>
                                        <div>
                                            <span class="name"> 课程要点： </span>
                                            <span class="val"> {{ map.kechengyaodian }} </span>
                                        </div>
                                        <div>
                                            <span class="name"> 发布教师： </span>
                                            <span class="val"> {{ map.fabujiaoshi }} </span>
                                        </div>
                                        <div>
                                            <span class="name"> 发布时间： </span>
                                            <span class="val"> {{ map.addtime }} </span>
                                        </div>
                                    </div>

                                    <e-chat-check :rid="map.fabujiaoshi">咨询教师</e-chat-check>
                                    <el-button type="primary"    v-if="$session.cx == '学生'"  @click="$router.push('/kechengxuexi/add?id='+map.id)">课程学习
                                    </el-button>
                                    <e-collect
                                            v-if="$session.cx == '学生'"
                                        module="shoucang"
                                        :form="{biaoid:'xwid',biao:'biao',biaoti:'biaoti'}"
                                        :biaoid="$route.query.id"
                                        biao="kechengxinxi"
                                        :biaoti="map.kechengmingcheng"
                                    >
                                        <template #icon="{isCollect}">
                                            <i class="fa" :class="isCollect?'fa-star' : 'fa-star-o'"></i>
                                        </template>
                                        <template #default="{isCollect}"> {{ isCollect ? '取消收藏' : '收藏' }} </template>
                                    </e-collect>
                                </div>
                            </div>
                            <div class="goods-content" v-html="map.kechengxiangqing"></div>
                        </div>
                    </div>
                    <!-- /.sidebar-widget-body -->
                </div>
            </e-container>
        </div>
        
        <!-- Tabs section - Only show when not loading and no error -->
        <div v-if="!map.loading && !map.error">
            <e-container>
                <e-container>
                    <el-tabs type="border-card">
                        <el-tab-pane label="课程视频">
                            <div class="hotnews class3">
                                <ul class="a">
                                    <li v-for="(r,i) in kechengshipinlist">
                                        <router-link :to="{path:'/kechengshipin/detail',query:{id:r.id}}" class="clearfix"> {{ r.shipinmingcheng }} </router-link>
                                    </li>
                                </ul>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="课程资源">
                            <div class="list-table">
                                <table width="100%" border="1" class="table table-list table-bordered table-hover">
                                    <thead>
                                        <tr align="center">
                                            <th width="60" align="center">序号</th>
                                            <th>课程编号</th>
                                            <th>课程名称</th>
                                            <th>课程分类</th>
                                            <th>发布教师</th>
                                            <th>资源名称</th>
                                            <th>资源附件</th>
                                            <th>发布时间</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(r,i) in kechengziyuanlist">
                                            <td width="30" align="center">{{ i+1 }}</td>
                                            <td>{{ r.kechengbianhao }}</td>
                                            <td>{{ r.kechengmingcheng }}</td>
                                            <td><e-select-view module="kechengfenlei" :value="r.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view></td>
                                            <td>{{ r.fabujiaoshi }}</td>
                                            <td>{{ r.ziyuanmingcheng }}</td>
                                            <td><e-file-list v-model="r.ziyuanfujian"></e-file-list></td>
                                            <td>{{ r.addtime.substring(0,19) }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </el-tab-pane>
                        <el-tab-pane label="布置作业">
                            <div class="list-table">
                                <table width="100%" border="1" class="table table-list table-bordered table-hover">
                                    <thead>
                                        <tr align="center">
                                            <th width="60" align="center">序号</th>

                                            <th>课程名称</th>
                                            <th>课程分类</th>
                                            <th>发布教师</th>

                                            <th>截至日期</th>
                                            <th>作业名称</th>
                                            <th>作业附件</th>
                                            <th>已提交人数</th>


                                            <th width="80" align="center">操作</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(r,i) in buzhizuoyelist">
                                            <td width="30" align="center">{{ i+1 }}</td>

                                            <td>{{ r.kechengmingcheng }}</td>
                                            <td><e-select-view module="kechengfenlei" :value="r.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view></td>
                                            <td>{{ r.fabujiaoshi }}</td>

                                            <td>{{ r.jiezhiriqi }}</td>
                                            <td>{{ r.zuoyemingcheng }}</td>
                                            <td><e-file-list v-model="r.zuoyefujian"></e-file-list></td>
                                            <td>{{ r.yitijiaorenshu }}</td>

                                            <td align="center">
                                               <!-- <template v-if="map.tijiaozuoyeCount == 0">
                                                    <el-button type="primary" v-if="$session.cx == '学生'"  @click="$router.push('/tijiaozuoye/add?id='+r.id)">提交作业
                                                    </el-button>

                                                </template>
                                                <template v-else>
                                                    你已提交过！
                                                </template>-->
                                                <el-button type="primary" v-if="$session.cx == '学生'"  @click="$router.push('/tijiaozuoye/add?id='+r.id)">提交作业
                                                </el-button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </el-tab-pane>
                    </el-tabs>
                </e-container>
            </e-container>
        </div>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";
    import EShangpinban from "@/components/shangpin/shangpinban.vue";

    import { ref, reactive, watch, computed, onMounted } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import { session } from "@/utils/utils";
    import { extend } from "@/utils/extend";
    import { useKechengxinxiFindById, canKechengxinxiFindById } from "@/module";
    import { ElMessage } from "element-plus";
    import { useUserStore } from "@/stores";

    const route = useRoute();
    const router = useRouter();
    const userStore = useUserStore();
    
    const props = defineProps({
        id: {
            type: [Number, String],
        },
        isShowBtn: {
            type: Boolean,
            default: true,
        },
    });

    // 获取课程ID，优先使用props，其次使用route参数
    const courseId = computed(() => {
        // 尝试获取ID并转换为数字
        let id = props.id || route.query.id;
        console.log('计算courseId, 原始值:', id, '类型:', typeof id);
        
        // 确保ID是有效的数字
        if (id !== undefined && id !== null) {
            // 尝试将ID转换为整数
            try {
                id = parseInt(id, 10);
                if (isNaN(id)) {
                    console.warn('课程ID不是有效整数:', id);
                    return null;
                }
                console.log('计算courseId, 转换后:', id, '类型:', typeof id);
                return id;
            } catch (e) {
                console.warn('课程ID转换失败:', id, e);
                return null;
            }
        }
        
        return null;
    });

    // 获取详情页面的一行数据
    const map = reactive({
        // 预设默认属性，防止渲染错误
        id: null,
        kechengbianhao: '',
        kechengmingcheng: '',
        kechengfenlei: '',
        kechengfengmian: '',
        kechengyaodian: '',
        fabujiaoshi: '',
        kechengxiangqing: '',
        addtime: '',
        issh: '否',
        loading: true, // 添加加载状态
        error: null   // 添加错误状态
    });

    // 重试加载函数
    const retryLoading = async () => {
        map.loading = true;
        map.error = null;
        
        // 确保我们有有效的课程ID
        const id = courseId.value;
        console.log('重试加载课程ID:', id, '类型:', typeof id);
        
        if (!id) {
            map.error = '无效的课程ID，无法加载数据';
            map.loading = false;
            ElMessage({
                type: 'error',
                message: '无效的课程ID'
            });
            return;
        }
        
        // 使用直接的fetch请求绕过可能的问题
        try {
            // 导入config
            const configModule = await import('@/config');
            const config = configModule.default;
            
            console.log('使用直接fetch请求绕过可能的问题');
            const requestUrl = `${config.service_url}/kechengxinxi/findById/?id=${id}`;
            console.log('请求URL:', requestUrl);
            
            const response = await fetch(requestUrl, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${userStore.token}`,
                    'token': userStore.token,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            console.log('收到原始响应:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`HTTP错误! 状态: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('解析后的响应数据:', data);
            
            if (data && data.code === 0 && data.data) {
                console.log('请求成功，返回数据:', data.data);
                extend(map, data.data);
                map.loading = false;
                ElMessage({
                    type: 'success',
                    message: '数据已重新加载'
                });
                return;
            } else {
                throw new Error(data.msg || '服务器返回了一个无效的响应格式');
            }
        } catch (error) {
            console.error('重试加载失败:', error);
            map.error = error.message || '重新加载数据失败';
            map.loading = false;
            ElMessage({
                type: 'error',
                message: '重新加载失败: ' + (error.message || '未知错误')
            });
            
            // 尝试从本地数据库获取数据
            try {
                console.log('尝试从本地数据库获取数据:', id);
                const localData = await DB.name("kechengxinxi").where("id", id).find();
                
                if (localData && Object.keys(localData).length > 0) {
                    console.log('从本地获取数据成功:', localData);
                    extend(map, localData);
                    map.loading = false;
                    map.fromCache = true;
                    
                    ElMessage({
                        type: 'warning',
                        message: '显示的是本地缓存数据，可能不是最新内容'
                    });
                }
            } catch (dbError) {
                console.error('从本地数据库获取数据失败:', dbError);
            }
        }
    };
    
    // 初始加载数据
    const loadInitialData = async (id) => {
        if (!id) {
            console.warn('无效的课程ID:', id);
            map.error = '无效的课程ID';
            map.loading = false;
            return;
        }
        
        console.log('开始加载课程数据, ID:', id);
        map.loading = true;
        map.error = null;
        
        try {
            const result = await canKechengxinxiFindById(id);
            console.log('成功获取课程数据:', result);
            extend(map, result);
            map.id = id; // 确保ID被正确设置
            map.loading = false;
        } catch (error) {
            console.error('加载课程数据失败:', error);
            map.error = error.message || '加载课程数据失败';
            map.loading = false;
            
            // 尝试从本地获取
            try {
                console.log('尝试从本地数据库获取:', id);
                const localData = await DB.name("kechengxinxi").where("id", id).find();
                if (localData && Object.keys(localData).length > 0) {
                    console.log('从本地获取成功:', localData);
                    extend(map, localData);
                    map.loading = false;
                    map.fromCache = true;
                }
            } catch (dbError) {
                console.error('从本地获取失败:', dbError);
            }
        }
    };
    
    // 监听ID变更，自动重新加载数据
    watch(courseId, (newId) => {
        if (newId !== null) {
            loadInitialData(newId);
        }
    }, { immediate: true });

    // 定义响应式变量kechengshipinlist
    const kechengshipinlist = ref([]);
    const getkechengshipinlist = async () => {
        // 检查map.id是否有效
        if (!map.id) {
            console.warn('无法加载课程视频: 无效的课程ID');
            return;
        }
        
        try {
            console.log('加载课程视频数据, 课程ID:', map.id);
            // 获取课程视频数据,并赋值给kechengshipinlist变量
            kechengshipinlist.value = await DB.name("kechengshipin").where("kechengxinxiid", map.id).limit("4").order("id desc").select();
            console.log('课程视频数据加载完成:', kechengshipinlist.value.length, '条记录');
        } catch (error) {
            console.error('加载课程视频失败:', error);
            kechengshipinlist.value = [];
        }
    };
    
    // 监听map值变化后，并重新获取数据课程视频模块的数据
    watch(() => map.id, (newId) => {
        if (newId) {
            console.log('课程ID变更，重新加载视频数据:', newId);
            getkechengshipinlist();
        }
    }, { immediate: true });
    
    // 定义响应式变量kechengziyuanlist
    const kechengziyuanlist = ref([]);
    const getkechengziyuanlist = async () => {
        // 检查map.id是否有效
        if (!map.id) {
            console.warn('无法加载课程资源: 无效的课程ID');
            return;
        }
        
        try {
            console.log('加载课程资源数据, 课程ID:', map.id);
            // 获取课程资源数据,并赋值给kechengziyuanlist变量
            kechengziyuanlist.value = await DB.name("kechengziyuan").where("kechengxinxiid", map.id).limit("100").order("id desc").select();
            console.log('课程资源数据加载完成:', kechengziyuanlist.value.length, '条记录');
        } catch (error) {
            console.error('加载课程资源失败:', error);
            kechengziyuanlist.value = [];
        }
    };
    
    // 监听map值变化后，并重新获取数据课程资源模块的数据
    watch(() => map.id, (newId) => {
        if (newId) {
            console.log('课程ID变更，重新加载资源数据:', newId);
            getkechengziyuanlist();
        }
    }, { immediate: true });
    
    // 定义响应式变量buzhizuoyelist
    const buzhizuoyelist = ref([]);
    const getbuzhizuoyelist = async () => {
        // 检查map.id是否有效
        if (!map.id) {
            console.warn('无法加载布置作业: 无效的课程ID');
            return;
        }
        
        try {
            console.log('加载布置作业数据, 课程ID:', map.id);
            // 获取布置作业数据,并赋值给buzhizuoyelist变量
            buzhizuoyelist.value = await DB.name("buzhizuoye").where("kechengxinxiid", map.id).limit("4").order("yitijiaorenshu desc").select();
            console.log('布置作业数据加载完成:', buzhizuoyelist.value.length, '条记录');
        } catch (error) {
            console.error('加载布置作业失败:', error);
            buzhizuoyelist.value = [];
        }
    };
    
    // 监听map值变化后，并重新获取数据布置作业模块的数据
    watch(() => map.id, (newId) => {
        if (newId) {
            console.log('课程ID变更，重新加载作业数据:', newId);
            getbuzhizuoyelist();
        }
    }, { immediate: true });

    // 在组件挂载时添加调试输出
    onMounted(() => {
        console.log('课程详情组件挂载，当前ID:', courseId.value, '类型:', typeof courseId.value);
        
        // 如果URL没有有效ID，但用户已登录，则重定向到课程列表
        if (!courseId.value && userStore.isLogin()) {
            console.warn('组件挂载时无有效课程ID，重定向到课程列表');
            ElMessage({
                type: 'warning',
                message: '课程ID无效，已返回列表页'
            });
            router.push('/kechengxinxi/list');
            return;
        }
        
        // 重新检查课程ID并加载
        if (courseId.value && !map.id) {
            console.log('组件挂载时尝试直接获取课程数据');
            loadInitialData(courseId.value);
        }
        
        // 设置重试定时器，如果10秒后仍未加载成功，则尝试重新加载
        const retryTimer = setTimeout(() => {
            console.log('自动重试检查 - 课程ID:', courseId.value);
            if (map.loading) {
                console.log('数据加载超时，自动尝试重新加载');
                retryLoading();
            }
        }, 10000);
        
        // 组件卸载时清除定时器
        return () => {
            clearTimeout(retryTimer);
        };
    });
</script>

<style scoped lang="scss">
    .views-kechengxinxi-web-detail {
        .loading-container {
            padding: 30px;
            text-align: center;
            
            .loading-text {
                margin-top: 15px;
                font-size: 16px;
                color: #909399;
            }
        }
        
        .error-container {
            padding: 30px;
            text-align: center;
        }
    }
</style>
