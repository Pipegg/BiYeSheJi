from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pandas as pd
import logging
from .knowledge_graph import KnowledgeGraph
from .learner_profile import LearnerProfile
from ..LLMs.model_service import ModelService

logger = logging.getLogger(__name__)

class RecommendationStrategy:
    def __init__(self, knowledge_graph: KnowledgeGraph, learner_profile: LearnerProfile):
        """
        初始化推荐策略
        """
        self.knowledge_graph = knowledge_graph
        self.learner_profile = learner_profile
        self.model_service = ModelService()
        self.strategy_weights = {
            'knowledge_based': 0.4,
            'collaborative': 0.3,
            'content_based': 0.3
        }
        self.scaler = StandardScaler()

    def recommend_courses(self, student_id: str, course_data: pd.DataFrame, 
                        student_data: pd.DataFrame, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        混合推荐策略
        """
        try:
            # 1. 获取学习者画像
            learner_profile = self.learner_profile.update_profile(student_id, 
                self._get_learning_records(student_id, student_data))
            
            # 2. 获取已学习的课程
            learned_courses = set(student_data[student_data['学生ID'] == student_id]['课程ID'])
            
            # 3. 获取各策略的推荐结果
            knowledge_based_recs = self._knowledge_based_recommend(student_id, course_data, 
                                                                learned_courses, learner_profile)
            collaborative_recs = self._collaborative_recommend(student_id, course_data, 
                                                            student_data, learned_courses)
            content_based_recs = self._content_based_recommend(student_id, course_data, 
                                                            learned_courses, learner_profile)
            
            # 4. 融合推荐结果
            final_recommendations = self._merge_recommendations(
                knowledge_based_recs,
                collaborative_recs,
                content_based_recs,
                top_n
            )
            
            # 5. 生成推荐解释
            return self._add_explanations(final_recommendations, learner_profile)
            
        except Exception as e:
            logger.error(f"生成推荐失败: {e}")
            return []

    def _get_learning_records(self, student_id: str, student_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        获取学习记录
        """
        try:
            records = student_data[student_data['学生ID'] == student_id].to_dict('records')
            # 确保所有键都是字符串类型
            return [{str(k): v for k, v in record.items()} for record in records]
        except Exception as e:
            logger.error(f"获取学习记录失败: {e}")
            return []

    def _knowledge_based_recommend(self, student_id: str, course_data: pd.DataFrame,
                                learned_courses: set, learner_profile: Dict[str, Any]) -> List[Dict[str, float]]:
        """
        基于知识图谱的推荐
        """
        try:
            recommendations = {}
            
            # 1. 分析学习者当前知识水平
            cognitive_features = learner_profile.get('cognitive_features', {})
            mastery_level = cognitive_features.get('mastery_level', 0)
            
            # 2. 获取适合的课程
            for _, course in course_data.iterrows():
                if course['课程ID'] not in learned_courses:
                    # 获取课程难度信息
                    difficulty_info = self.knowledge_graph.get_course_difficulty(course['课程ID'])
                    
                    # 检查前置课程
                    prerequisites = self.knowledge_graph.get_course_prerequisites(course['课程ID'])
                    prereq_completed = all(pre['id'] in learned_courses for pre in prerequisites)
                    
                    if prereq_completed:
                        # 计算课程匹配度
                        difficulty_match = self._calculate_difficulty_match(mastery_level, difficulty_info)
                        knowledge_relevance = self._calculate_knowledge_relevance(course['课程ID'], 
                                                                              list(learned_courses))
                        
                        # 综合评分
                        score = 0.6 * difficulty_match + 0.4 * knowledge_relevance
                        recommendations[course['课程ID']] = score
            
            # 转换为列表格式
            return [{'course_id': k, 'score': v} for k, v in recommendations.items()]
            
        except Exception as e:
            logger.error(f"知识图谱推荐失败: {e}")
            return []

    def _collaborative_recommend(self, student_id: str, course_data: pd.DataFrame,
                              student_data: pd.DataFrame, learned_courses: set) -> List[Dict[str, float]]:
        """
        协同过滤推荐
        """
        try:
            # 1. 构建用户-课程矩阵
            user_course_matrix = pd.pivot_table(
                student_data,
                values='学习进度',
                index='学生ID',
                columns='课程ID',
                fill_value=0
            )
            
            # 2. 计算用户相似度
            user_similarity = cosine_similarity(user_course_matrix)
            user_similarity_df = pd.DataFrame(
                user_similarity,
                index=user_course_matrix.index,
                columns=user_course_matrix.index
            )
            
            # 3. 找到相似用户
            similar_users = user_similarity_df[student_id].sort_values(ascending=False)[1:6]
            
            # 4. 获取推荐课程
            recommendations = {}
            for similar_user, similarity in similar_users.items():
                # 获取相似用户完成的课程
                user_courses = set(student_data[student_data['学生ID'] == similar_user]['课程ID'])
                
                # 推荐未学习的课程
                for course_id in user_courses - learned_courses:
                    if course_id not in recommendations:
                        recommendations[course_id] = 0
                    recommendations[course_id] += similarity
            
            return [{'course_id': k, 'score': v} for k, v in recommendations.items()]
            
        except Exception as e:
            logger.error(f"协同过滤推荐失败: {e}")
            return []

    def _content_based_recommend(self, student_id: str, course_data: pd.DataFrame,
                              learned_courses: set, learner_profile: Dict[str, Any]) -> List[Dict[str, float]]:
        """
        基于内容的推荐
        """
        try:
            recommendations = {}
            
            # 1. 获取学习者兴趣特征
            interest_areas = learner_profile.get('affective_features', {}).get('interest_areas', [])
            learning_style = learner_profile.get('affective_features', {}).get('learning_style', '')
            
            # 2. 分析每个未学习课程的匹配度
            for _, course in course_data.iterrows():
                if course['课程ID'] not in learned_courses:
                    # 计算兴趣匹配度
                    interest_match = self._calculate_interest_match(course, interest_areas)
                    
                    # 计算学习风格匹配度
                    style_match = self._calculate_style_match(course, learning_style)
                    
                    # 综合评分
                    score = 0.7 * interest_match + 0.3 * style_match
                    recommendations[course['课程ID']] = score
            
            return [{'course_id': k, 'score': v} for k, v in recommendations.items()]
            
        except Exception as e:
            logger.error(f"基于内容推荐失败: {e}")
            return []

    def _calculate_difficulty_match(self, mastery_level: float, 
                                 difficulty_info: Dict[str, Any]) -> float:
        """
        计算难度匹配度
        """
        try:
            base_difficulty = difficulty_info.get('base_difficulty', 'medium')
            skill_levels = difficulty_info.get('skill_levels', [])
            
            # 难度等级映射
            difficulty_map = {'easy': 0.3, 'medium': 0.5, 'hard': 0.8}
            course_difficulty = difficulty_map.get(base_difficulty, 0.5)
            
            # 计算技能等级匹配度
            skill_match = 0.0
            if skill_levels:
                skill_levels_num = [difficulty_map.get(level, 0.5) for level in skill_levels]
                skill_match = float(np.mean(skill_levels_num))
            
            # 计算总体匹配度
            diff = abs(mastery_level - course_difficulty)
            match_score = 1.0 - diff
            
            return float(0.7 * match_score + 0.3 * skill_match)
            
        except Exception as e:
            logger.error(f"计算难度匹配失败: {e}")
            return 0.5

    def _calculate_knowledge_relevance(self, course_id: str, learned_courses: List[str]) -> float:
        """
        计算知识关联度
        """
        try:
            relevance_scores = []
            
            for learned_course in learned_courses:
                # 获取知识路径
                path = self.knowledge_graph.get_knowledge_path(learned_course, course_id)
                
                if path:
                    # 路径越短，关联度越高
                    relevance_scores.append(1.0 / len(path))
            
            return max(relevance_scores) if relevance_scores else 0.0
            
        except Exception as e:
            logger.error(f"计算知识关联度失败: {e}")
            return 0.0

    def _calculate_interest_match(self, course: pd.Series, interest_areas: List[str]) -> float:
        """
        计算兴趣匹配度
        """
        try:
            if not interest_areas:
                return 0.5
                
            course_category = course['课程分类']
            
            # 计算类别匹配度
            category_match = 1.0 if course_category in interest_areas else 0.3
            
            # 使用大模型分析课程描述与兴趣的匹配度
            prompt = f"""
            分析以下课程描述与学习者兴趣领域的匹配程度：
            
            课程描述：{course['课程描述']}
            兴趣领域：{', '.join(interest_areas)}
            
            请返回0到1之间的匹配度分数。
            """
            
            content_match = float(self.model_service.generate_response(prompt) or 0.5)
            
            return 0.4 * category_match + 0.6 * content_match
            
        except Exception as e:
            logger.error(f"计算兴趣匹配度失败: {e}")
            return 0.5

    def _calculate_style_match(self, course: pd.Series, learning_style: str) -> float:
        """
        计算学习风格匹配度
        """
        try:
            if not learning_style:
                return 0.5
                
            # 分析课程资源类型与学习风格的匹配度
            prompt = f"""
            分析以下课程与学习风格的匹配程度：
            
            课程信息：{course.to_dict()}
            学习风格：{learning_style}
            
            请返回0到1之间的匹配度分数。
            """
            
            return float(self.model_service.generate_response(prompt) or 0.5)
            
        except Exception as e:
            logger.error(f"计算学习风格匹配度失败: {e}")
            return 0.5

    def _merge_recommendations(self, knowledge_based: List[Dict[str, float]],
                            collaborative: List[Dict[str, float]],
                            content_based: List[Dict[str, float]],
                            top_n: int) -> List[Dict[str, Any]]:
        """
        融合各种推荐结果
        """
        try:
            # 1. 创建课程得分字典
            course_scores = {}
            
            # 2. 合并知识图谱推荐结果
            for rec in knowledge_based:
                course_id = rec['course_id']
                score = rec['score'] * self.strategy_weights['knowledge_based']
                course_scores[course_id] = course_scores.get(course_id, 0) + score
            
            # 3. 合并协同过滤推荐结果
            for rec in collaborative:
                course_id = rec['course_id']
                score = rec['score'] * self.strategy_weights['collaborative']
                course_scores[course_id] = course_scores.get(course_id, 0) + score
            
            # 4. 合并基于内容的推荐结果
            for rec in content_based:
                course_id = rec['course_id']
                score = rec['score'] * self.strategy_weights['content_based']
                course_scores[course_id] = course_scores.get(course_id, 0) + score
            
            # 5. 排序并返回前N个推荐
            sorted_courses = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)
            return [{'course_id': course_id, 'score': score} 
                   for course_id, score in sorted_courses[:top_n]]
            
        except Exception as e:
            logger.error(f"融合推荐结果失败: {e}")
            return []

    def _add_explanations(self, recommendations: List[Dict[str, Any]], 
                        learner_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        添加推荐解释
        """
        try:
            for rec in recommendations:
                course_id = rec['course_id']
                
                # 获取课程信息
                course_info = self.knowledge_graph.get_course_knowledge_points(course_id)
                prerequisites = self.knowledge_graph.get_course_prerequisites(course_id)
                
                # 生成解释
                prompt = f"""
                基于以下信息生成课程推荐解释：
                
                课程信息：
                - 知识点：{course_info}
                - 前置课程：{prerequisites}
                
                学习者画像：
                {learner_profile}
                
                推荐分数：{rec['score']}
                
                请从以下方面解释推荐原因：
                1. 与学习者当前水平的匹配度
                2. 与学习者兴趣的契合度
                3. 在知识体系中的重要性
                4. 对能力提升的帮助
                """
                
                explanation = self.model_service.generate_response(prompt)
                rec['explanation'] = explanation if explanation else "无法生成推荐解释"
            
            return recommendations
            
        except Exception as e:
            logger.error(f"生成推荐解释失败: {e}")
            return recommendations 