# =====================
# 依赖导入
# =====================
from typing import List, Dict, Any, Optional
import pandas as pd
import networkx as nx
from ..LLMs.model_service import ModelService

# =====================
# LLM 驱动的智能推荐系统
# =====================
class LLMRecommender:
    def __init__(self):
        """
        初始化基于大模型的推荐系统
        """
        self.model_service = ModelService()
        self.course_data: Optional[pd.DataFrame] = None
        self.student_data: Optional[pd.DataFrame] = None
        self.knowledge_graph = nx.DiGraph()
        
    # =====================
    # 知识图谱构建
    # =====================
    def build_knowledge_graph(self) -> None:
        """
        构建课程知识图谱
        """
        if self.course_data is None or self.course_data.empty:
            return
            
        # 让大模型分析课程之间的关系
        course_list = self.course_data.to_dict('records')
        for i, course1 in enumerate(course_list):
            for j, course2 in enumerate(course_list):
                if i >= j:  # 避免重复分析
                    continue
                    
                prompt = f"""分析以下两门课程之间的关系：
                课程1：{course1['课程名称']}
                描述：{course1['课程描述']}               
                课程2：{course2['课程名称']}
                描述：{course2['课程描述']}                
                请分析它们之间的关系，包括：
                1. 是否存在前置关系
                2. 知识点的关联程度（0-1）
                3. 学习路径上的关系               
                请以JSON格式返回：
                {
                    "prerequisite": true/false,
                    "relevance": 0.8,
                    "path_relationship": "进阶/并行/独立"
                }
                """
                
                try:
                    response = self.model_service.generate_structured_response(prompt)
                    if response:
                        # 添加到知识图谱
                        self.knowledge_graph.add_edge(
                            course1['课程ID'],
                            course2['课程ID'],
                            weight=float(response.get('relevance', 0)),
                            prerequisite=bool(response.get('prerequisite', False)),
                            relationship=str(response.get('path_relationship', '独立'))
                        )
                except Exception as e:
                    print(f"分析课程关系时出错: {e}")

    # =====================
    # 学生画像分析
    # =====================
    def analyze_student_profile(self, student_id: str) -> Dict[str, Any]:
        """
        多维度分析学生学习画像
        """
        if self.student_data is None or self.course_data is None:
            return {"type": "new_user"}
            
        try:
            student_records = self.student_data[self.student_data['学生ID'] == student_id]
            if len(student_records) == 0:
                return {"type": "new_user"}
                
            # 收集学习数据
            learning_data = {
                "completed_courses": [],
                "learning_progress": [],
                "learning_time": [],
                "quiz_scores": [],
                "interaction_records": []
            }
            
            for _, record in student_records.iterrows():
                course_matches = self.course_data[self.course_data['课程ID'] == record['课程ID']]
                if not course_matches.empty:
                    course_info = course_matches.iloc[0]
                    learning_data["completed_courses"].append({
                        "course_name": str(course_info['课程名称']),
                        "category": str(course_info['课程分类']),
                        "progress": float(record['学习进度']),
                        "time_spent": float(record.get('学习时长', 0)),
                        "quiz_score": float(record.get('测试分数', 0)),
                        "interactions": int(record.get('互动次数', 0))
                    })
                    
            # 让大模型分析学习画像
            prompt = f"""请分析以下学生的学习数据，生成完整的学习画像：           
            学习数据：{learning_data}           
            请分析以下方面：
            1. 学习风格
            2. 知识掌握水平
            3. 学习兴趣点
            4. 学习习惯
            5. 优势和不足
            6. 发展建议           
            请以JSON格式返回分析结果。
            """
            
            response = self.model_service.generate_structured_response(prompt)
            return response if response else {"type": "analysis_failed"}
            
        except Exception as e:
            print(f"分析学生画像时出错: {e}")
            return {"type": "error", "message": str(e)}

    # =====================
    # 课程前置关系
    # =====================
    def get_course_prerequisites(self, course_id: str) -> List[str]:
        """
        获取课程的前置课程
        """
        if not self.knowledge_graph.has_node(course_id):
            return []
            
        prerequisites = []
        try:
            for pred in self.knowledge_graph.predecessors(course_id):
                edge_data = self.knowledge_graph.get_edge_data(pred, course_id)
                if edge_data and edge_data.get('prerequisite', False):
                    prerequisites.append(pred)
        except Exception as e:
            print(f"获取课程前置需求时出错: {e}")
            
        return prerequisites

    # =====================
    # 推荐主流程
    # =====================
    def recommend_courses(self, student_id: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        基于知识图谱和学习画像推荐课程
        """
        if self.course_data is None or self.student_data is None:
            return []

        try:
            # 1. 获取学生多维度画像
            student_profile = self.analyze_student_profile(student_id)
            
            # 2. 获取已学习的课程
            learned_courses = set()
            student_records = self.student_data[self.student_data['学生ID'] == student_id]
            learned_courses = set(student_records['课程ID'].unique())
            
            # 3. 构建推荐提示词
            available_courses = []
            for _, course in self.course_data.iterrows():
                if course['课程ID'] not in learned_courses:
                    prerequisites = self.get_course_prerequisites(str(course['课程ID']))
                    course_info = {
                        'name': str(course['课程名称']),
                        'category': str(course['课程分类']),
                        'description': str(course['课程描述']),
                        'prerequisites': prerequisites
                    }
                    available_courses.append(course_info)

            prompt = f"""作为智能教育顾问，请基于以下信息推荐课程：
            学生画像：
            {student_profile}           
            已学习课程：{list(learned_courses)}           
            可选课程：
            {available_courses}           
            请推荐最适合该学生的{top_n}门课程，并详细说明推荐原因。考虑：
            1. 与学生当前水平的匹配度
            2. 与学生兴趣的契合度
            3. 在知识图谱中的关联性
            4. 学习路径的合理性           
            请以JSON格式返回：
            {
                "recommendations": [
                    {
                        "course_name": "课程名称",
                        "reason": "详细的推荐原因",
                        "difficulty_match": "难度匹配分析",
                        "interest_match": "兴趣匹配分析",
                        "knowledge_path": "知识路径分析"
                    }
                ]
            }
            """
            
            # 4. 获取推荐结果
            response = self.model_service.generate_structured_response(prompt)
            
            # 5. 处理推荐结果
            recommendations = []
            if response and 'recommendations' in response:
                for rec in response['recommendations']:
                    course_matches = self.course_data[self.course_data['课程名称'] == rec['course_name']]
                    if not course_matches.empty:
                        course_info = course_matches.iloc[0]
                        recommendations.append({
                            'course_id': str(course_info['课程ID']),
                            'course_name': str(rec['course_name']),
                            'description': str(course_info['课程描述']),
                            'reason': str(rec['reason']),
                            'difficulty_match': str(rec.get('difficulty_match', '')),
                            'interest_match': str(rec.get('interest_match', '')),
                            'knowledge_path': str(rec.get('knowledge_path', ''))
                        })
            
            return recommendations[:top_n]
            
        except Exception as e:
            print(f"推荐课程时出错: {e}")
            return []

    # =====================
    # 推荐解释
    # =====================
    def get_recommendation_explanation(self, student_id: str, course_id: str) -> str:
        """
        获取推荐原因的详细解释
        """
        if self.course_data is None:
            return "无法获取课程信息"
            
        try:
            course_matches = self.course_data[self.course_data['课程ID'] == course_id]
            if course_matches.empty:
                return "未找到课程信息"
                
            course_info = course_matches.iloc[0]
            student_profile = self.analyze_student_profile(student_id)
            
            prompt = f"""请详细解释为什么向该学生推荐这门课程：
            课程信息：
            {course_info.to_dict()}            
            学生画像：
            {student_profile}            
            请从以下方面进行解释：
            1. 与学生当前学习阶段的适配性
            2. 与学生兴趣特点的匹配度
            3. 在整体学习路径中的作用
            4. 对学生能力提升的帮助
            5. 具体的学习建议
            """
            
            explanation = self.model_service.generate_response(prompt)
            return explanation if explanation else "无法生成推荐解释"
            
        except Exception as e:
            print(f"获取推荐解释时出错: {e}")
            return f"生成推荐解释时发生错误: {str(e)}"

    # =====================
    # 数据加载与知识图谱构建
    # =====================
    def fit(self, course_data: pd.DataFrame, student_data: pd.DataFrame) -> None:
        """
        加载数据并构建知识图谱
        """
        try:
            self.course_data = course_data.copy()
            self.student_data = student_data.copy()
            self.build_knowledge_graph()
        except Exception as e:
            print(f"加载数据时出错: {e}")
            self.course_data = None
            self.student_data = None

    # =====================
    # 热门课程分析
    # =====================
    def get_popular_courses(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        获取热门课程，使用大模型分析受欢迎原因
        """
        if self.student_data is None or self.course_data is None:
            return []
            
        try:
            # 1. 获取学习人数最多的课程
            course_counts = self.student_data['课程ID'].value_counts()[:top_n]
            popular_courses = []
            
            for course_id, count in course_counts.items():
                course_matches = self.course_data[self.course_data['课程ID'] == course_id]
                if course_matches.empty:
                    continue
                    
                course_info = course_matches.iloc[0]
                
                # 2. 分析课程在知识图谱中的位置
                graph_position = {
                    'centrality': float(nx.degree_centrality(self.knowledge_graph).get(course_id, 0)),
                    'prerequisites': self.get_course_prerequisites(str(course_id))
                }
                
                # 3. 让大模型分析课程特点
                prompt = f"""分析以下课程的特点和受欢迎原因：                
                课程信息：
                - 名称：{course_info['课程名称']}
                - 分类：{course_info['课程分类']}
                - 描述：{course_info['课程描述']}
                - 学习人数：{count}人               
                知识图谱位置：
                - 中心度：{graph_position['centrality']}
                - 前置课程：{graph_position['prerequisites']}                
                请分析该课程受欢迎的原因，包括：
                1. 课程内容特点
                2. 在知识体系中的地位
                3. 对学生的实际帮助
                """
                
                analysis = self.model_service.generate_response(prompt)
                
                popular_courses.append({
                    'course_id': str(course_id),
                    'course_name': str(course_info['课程名称']),
                    'description': str(course_info['课程描述']),
                    'study_count': int(count),
                    'popularity_reason': str(analysis) if analysis else "无法生成分析",
                    'graph_position': graph_position
                })
                
            return popular_courses
            
        except Exception as e:
            print(f"获取热门课程时出错: {e}")
            return [] 