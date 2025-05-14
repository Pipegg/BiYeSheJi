<template>
  <div class="course-recommendation">
    <a-card title="课程推荐" :bordered="false">
      <template #extra>
        <a-button type="link" @click="refreshRecommendations">
          <reload-outlined />刷新推荐
        </a-button>
      </template>
      
      <a-spin :spinning="loading">
        <div class="recommendation-container">
          <!-- 个性化推荐课程 -->
          <div class="recommendation-section" v-if="recommendations.length">
            <h3>为您推荐</h3>
            <a-row :gutter="16">
              <a-col :span="8" v-for="course in recommendations" :key="course.course_id">
                <a-card hoverable class="course-card">
                  <template #cover>
                    <img
                      alt="课程封面"
                      :src="course.cover || '/default-course-cover.jpg'"
                    />
                  </template>
                  <a-card-meta :title="course.course_name">
                    <template #description>
                      <div class="course-description">{{ course.description }}</div>
                      <div class="recommendation-reason">
                        <info-circle-outlined /> {{ course.reason }}
                      </div>
                    </template>
                  </a-card-meta>
                  <template #actions>
                    <a-button type="primary" @click="startLearning(course.course_id)">
                      开始学习
                    </a-button>
                  </template>
                </a-card>
              </a-col>
            </a-row>
          </div>

          <!-- 热门课程 -->
          <div class="recommendation-section">
            <h3>热门课程</h3>
            <a-row :gutter="16">
              <a-col :span="8" v-for="course in popularCourses" :key="course.course_id">
                <a-card hoverable class="course-card">
                  <template #cover>
                    <img
                      alt="课程封面"
                      :src="course.cover || '/default-course-cover.jpg'"
                    />
                  </template>
                  <a-card-meta :title="course.course_name">
                    <template #description>
                      <div class="course-description">{{ course.description }}</div>
                      <div class="study-count">
                        <team-outlined /> {{ course.study_count }}人学习
                      </div>
                    </template>
                  </a-card-meta>
                  <template #actions>
                    <a-button type="primary" @click="startLearning(course.course_id)">
                      开始学习
                    </a-button>
                  </template>
                </a-card>
              </a-col>
            </a-row>
          </div>
        </div>
      </a-spin>
    </a-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import {
  ReloadOutlined,
  InfoCircleOutlined,
  TeamOutlined
} from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default defineComponent({
  name: 'CourseRecommendation',
  components: {
    ReloadOutlined,
    InfoCircleOutlined,
    TeamOutlined
  },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const recommendations = ref([]);
    const popularCourses = ref([]);

    const fetchRecommendations = async () => {
      loading.value = true;
      try {
        const response = await axios.get('/api/yuce/recommend_courses/');
        if (response.data.code === 0) {
          recommendations.value = response.data.data;
        } else {
          message.error(response.data.msg || '获取推荐失败');
        }
      } catch (error) {
        message.error('获取推荐失败');
        console.error(error);
      } finally {
        loading.value = false;
      }
    };

    const fetchPopularCourses = async () => {
      try {
        const response = await axios.get('/api/yuce/get_popular_courses/');
        if (response.data.code === 0) {
          popularCourses.value = response.data.data;
        } else {
          message.error(response.data.msg || '获取热门课程失败');
        }
      } catch (error) {
        message.error('获取热门课程失败');
        console.error(error);
      }
    };

    const refreshRecommendations = async () => {
      await fetchRecommendations();
      message.success('推荐已更新');
    };

    const startLearning = (courseId) => {
      router.push(`/course/${courseId}`);
    };

    onMounted(() => {
      fetchRecommendations();
      fetchPopularCourses();
    });

    return {
      loading,
      recommendations,
      popularCourses,
      refreshRecommendations,
      startLearning
    };
  }
});
</script>

<style scoped>
.course-recommendation {
  padding: 24px;
}

.recommendation-container {
  margin-top: 16px;
}

.recommendation-section {
  margin-bottom: 32px;
}

.recommendation-section h3 {
  margin-bottom: 16px;
  color: #1890ff;
}

.course-card {
  margin-bottom: 16px;
}

.course-description {
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.recommendation-reason,
.study-count {
  color: #1890ff;
  font-size: 12px;
}

.ant-card-cover img {
  height: 160px;
  object-fit: cover;
}
</style> 