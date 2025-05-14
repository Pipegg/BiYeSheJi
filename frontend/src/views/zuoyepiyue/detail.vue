<template>
    <div class="homework-evaluation">
        <el-card class="evaluation-card">
            <template #header>
                <div class="card-header">
                    <h2>作业批改结果</h2>
                </div>
            </template>

            <div class="evaluation-content">
                <div class="basic-info">
                    <el-descriptions :column="2" border>
                        <el-descriptions-item label="作业名称">{{ homework.zuoyemingcheng }}</el-descriptions-item>
                        <el-descriptions-item label="课程名称">{{ homework.kechengmingcheng }}</el-descriptions-item>
                        <el-descriptions-item label="提交学生">{{ homework.xueshengxingming }}</el-descriptions-item>
                        <el-descriptions-item label="提交时间">{{ homework.addtime }}</el-descriptions-item>
                    </el-descriptions>
                </div>

                <div class="score-section">
                    <el-progress
                        type="dashboard"
                        :percentage="evaluation.score"
                        :color="scoreColor"
                        :format="scoreFormat"
                    >
                        <template #default="{ percentage }">
                            <div class="score-value">
                                <span class="score">{{ percentage }}</span>
                                <span class="score-label">分</span>
                            </div>
                        </template>
                    </el-progress>
                </div>

                <div class="evaluation-details">
                    <el-collapse v-model="activeNames">
                        <el-collapse-item title="优点" name="strengths">
                            <ul class="strength-list">
                                <li v-for="(strength, index) in evaluation.strengths" :key="index">
                                    {{ strength }}
                                </li>
                            </ul>
                        </el-collapse-item>

                        <el-collapse-item title="需要改进的地方" name="weaknesses">
                            <ul class="weakness-list">
                                <li v-for="(weakness, index) in evaluation.weaknesses" :key="index">
                                    {{ weakness }}
                                </li>
                            </ul>
                        </el-collapse-item>

                        <el-collapse-item title="具体建议" name="suggestions">
                            <ul class="suggestion-list">
                                <li v-for="(suggestion, index) in evaluation.suggestions" :key="index">
                                    {{ suggestion }}
                                </li>
                            </ul>
                        </el-collapse-item>
                    </el-collapse>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script setup>
    import http from "@/utils/ajax/http";
    import DB from "@/utils/db";

    import { ref, reactive, watch, computed, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import { session } from "@/utils/utils";
    import { extend } from "@/utils/extend";
    import { useZuoyepiyueFindById, canZuoyepiyueFindById } from "@/module";
    import { ElMessage } from 'element-plus'

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
    const map = useZuoyepiyueFindById(props.id);
    // 当url参数id变更时，自动更新map中的数据
    watch(
        () => props.id,
        (id) => {
            canZuoyepiyueFindById(id).then((res) => {
                extend(map, res);
            });
        }
    );
    // end 获取详情页面的一行数据

    const homework = ref({})
    const evaluation = ref({
        score: 0,
        strengths: [],
        weaknesses: [],
        suggestions: []
    })
    const activeNames = ref(['strengths', 'weaknesses', 'suggestions'])

    // 计算分数颜色
    const scoreColor = computed(() => {
        const score = evaluation.value.score
        if (score >= 90) return '#67C23A'
        if (score >= 80) return '#E6A23C'
        if (score >= 60) return '#F56C6C'
        return '#909399'
    })

    // 格式化分数显示
    const scoreFormat = (percentage) => {
        return `${percentage}分`
    }

    // 加载作业信息
    const loadHomework = async () => {
        try {
            const response = await http.get('/tijiaozuoye/findById/', {
                id: route.query.id
            })
            if (response.code === 0) {
                homework.value = response.data
                // 加载AI批改结果
                await loadEvaluation()
            } else {
                ElMessage.error(response.msg || '获取作业信息失败')
            }
        } catch (error) {
            ElMessage.error('网络错误，请稍后重试')
        }
    }

    // 加载批改结果
    const loadEvaluation = async () => {
        try {
            const response = await http.get('/ai_service/homework-evaluation/', {
                homework_id: homework.value.id
            })
            if (response.code === 0) {
                evaluation.value = response.data
            } else {
                ElMessage.error(response.msg || '获取批改结果失败')
            }
        } catch (error) {
            ElMessage.error('网络错误，请稍后重试')
        }
    }

    onMounted(() => {
        loadHomework()
    })
</script>

<style scoped lang="scss">
    .homework-evaluation {
        padding: 20px;

        .evaluation-card {
            .card-header {
                text-align: center;
                h2 {
                    margin: 0;
                    color: #409EFF;
                }
            }

            .evaluation-content {
                .basic-info {
                    margin-bottom: 30px;
                }

                .score-section {
                    text-align: center;
                    margin: 30px 0;

                    .score-value {
                        .score {
                            font-size: 28px;
                            font-weight: bold;
                        }
                        .score-label {
                            font-size: 14px;
                            color: #909399;
                        }
                    }
                }

                .evaluation-details {
                    ul {
                        list-style: none;
                        padding: 0;
                        margin: 0;

                        li {
                            padding: 8px 0;
                            border-bottom: 1px solid #EBEEF5;

                            &:last-child {
                                border-bottom: none;
                            }
                        }
                    }

                    .strength-list li {
                        color: #67C23A;
                    }

                    .weakness-list li {
                        color: #F56C6C;
                    }

                    .suggestion-list li {
                        color: #409EFF;
                    }
                }
            }
        }
    }
</style>
