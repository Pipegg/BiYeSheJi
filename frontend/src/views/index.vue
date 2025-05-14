<template>
    <div class="views-zhuye">
        <div>
            <e-container>
                <el-carousel indicator-position="outside" height="520px">
                    <el-carousel-item v-for="item in bhtList" :key="item.id">
                        <a href="javascript:;">
                            <div
                                style="background-size: cover"
                                @click="$goto(item.url)"
                                :style="{'background-image': 'url('+$formatImageSrc(item.image)+')',width:'100%', height: '520px'}"
                            ></div>
                        </a>
                    </el-carousel-item>
                </el-carousel>
            </e-container>
        </div>
        <div>
            <e-container>
                <div class="title-modelbox-widget">
                    <h3 class="section-title">课程推荐</h3>
                    <div class="sidebar-widget-body">
                        <el-row :gutter="15">
                            <el-col v-for="r in kechengxinxilist" :md="6" :key="r.id" style="margin-bottom: 20px">
                                <div class="photo-content">
                                    <router-link class="thumbs" :to="'/kechengxinxi/detail?id='+r.id">
                                        <e-img :src="r.kechengfengmian" :pb="100"></e-img>
                                    </router-link>
                                    <div class="photo-content-text">
                                        <router-link :to="'/kechengxinxi/detail?id='+r.id">
                                            <h3>{{ r.kechengmingcheng }}</h3>
                                        </router-link>
                                        <div class="description" v-if="r.kechengxiangqing" v-text="$substr(r.kechengxiangqing , 30)"></div>
                                        <div class="other-content">
                                            <span>
                                                课程分类: <e-select-view module="kechengfenlei" :value="r.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view>
                                            </span>
                                            <span>课程要点:{{ r.kechengyaodian }}</span>
                                        </div>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <!-- /.sidebar-widget-body -->
                </div>

                <div class="title-modelbox-widget">
                    <h3 class="section-title">课程信息</h3>
                    <div class="sidebar-widget-body">
                        <el-row :gutter="15">
                            <el-col v-for="r in kechengxinxilist1" :md="6" :key="r.id" style="margin-bottom: 20px">
                                <div class="photo-content">
                                    <router-link class="thumbs" :to="'/kechengxinxi/detail?id='+r.id">
                                        <e-img :src="r.kechengfengmian" :pb="100"></e-img>
                                    </router-link>
                                    <div class="photo-content-text">
                                        <router-link :to="'/kechengxinxi/detail?id='+r.id">
                                            <h3>{{ r.kechengmingcheng }}</h3>
                                        </router-link>
                                        <div class="description" v-if="r.kechengxiangqing" v-text="$substr(r.kechengxiangqing , 30)"></div>
                                        <div class="other-content">
                                            <span
                                                >课程分类: <e-select-view module="kechengfenlei" :value="r.kechengfenlei" select="id" show="fenleimingcheng"></e-select-view
                                            ></span>
                                            <span>课程要点:{{ r.kechengyaodian }}</span>
                                        </div>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <!-- /.sidebar-widget-body -->
                </div>
            </e-container>
        </div>
        <div>
            <e-container>
                <div class="title-modelbox-widget">
                    <h3 class="section-title">交流论坛</h3>
                    <div class="sidebar-widget-body">
                        <el-row :gutter="15">
                            <el-col v-for="r in luntanjiaoliulist" :md="6" :key="r.id" style="margin-bottom: 20px">
                                <div class="photo-content">
                                    <router-link class="thumbs" :to="'/luntanjiaoliu/detail?id='+r.id">
                                        <e-img :src="r.tupian" :pb="100"></e-img>
                                    </router-link>
                                    <div class="photo-content-text">
                                        <router-link :to="'/luntanjiaoliu/detail?id='+r.id">
                                            <h3>{{ r.biaoti }}</h3>
                                        </router-link>
                                        <div class="description" v-if="r.hudongneirong" v-text="$substr(r.hudongneirong , 30)"></div>
                                        <div class="other-content">
                                            <span>分类: <e-select-view module="luntanfenlei" :value="r.fenlei" select="id" show="fenleimingcheng"></e-select-view></span>
                                            <span>回复数:{{ r.huifushu }}</span>
                                        </div>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
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
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import {httpPost} from "@/utils/ajax";
    import config from "@/config";

    // 获取路由
    const route = useRoute(); 

    // 获取轮播图信息
    const bhtList = DB.name("lunbotu").order("id desc").limit(5).selectRef();

    // 定义响应式变量kechengxinxilist,并获取数据课程信息模块的数据
    const kechengxinxilist = ref([]);
    const loadKechengxinxi = () => {
        // 直接使用DB对象查询课程信息
        DB.name("kechengxinxi")
          .limit(8)
          .order("id desc")
          .select()
          .then(res => {
              if (res && Array.isArray(res) && res.length > 0) {
                  kechengxinxilist.value = res;
              } else {
                  // 如果未获取到数据，使用测试数据
                  console.log("未获取到数据");
              }
          })
          .catch(err => {
              // 出错时使用测试数据
              console.log("未获取到数据");
          });
    }

    // 课程信息和论坛变量
    const kechengxinxilist1 = ref([]);
    const luntanjiaoliulist = ref([]);
    
    // 初始化加载
    onMounted(() => {
        // 加载课程推荐数据
        loadKechengxinxi();
        
        // 加载课程信息数据
        DB.name("kechengxinxi")
          .limit(8)
          .order("id desc")
          .select()
          .then(res => {
              if (res && Array.isArray(res) && res.length > 0) {
                  kechengxinxilist1.value = res;
              }
          });
        
        // 加载论坛交流数据
        DB.name("luntanjiaoliu")
          .limit(8)
          .order("huifushu desc")
          .select()
          .then(res => {
              if (res && Array.isArray(res) && res.length > 0) {
                  luntanjiaoliulist.value = res;
              }
          });
    });
</script>

<style scoped lang="scss">
    .views-zhuye {
        // 暂时没有样式
        .el-carousel__container {
            height: 520px;
        }
    }
</style>
