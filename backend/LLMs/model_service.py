from typing import Dict, Any, List, Optional
from .qwen_model import QwenModel
from .utils import parse_json_response, validate_response
import json

class ModelService:
    def __init__(self):
        """初始化模型服务"""
        self.model = QwenModel()
        # 存储对话上下文
        self.conversation_contexts: Dict[str, List[Dict]] = {}

    def answer_question(self, question: str, user_id: str, context: str = "") -> str:
        """
        回答用户问题，支持上下文理解和多轮对话
        
        Args:
            question: 用户问题
            user_id: 用户ID
            context: 额外的上下文信息
        
        Returns:
            str: AI的回答
        """
        try:
            # 获取用户的对话历史
            history = self.conversation_contexts.get(user_id, [])
            
            # 构建提示词
            prompt = "你是一个专业的AI学习助手，擅长解答学习问题。请根据以下信息回答问题：\n\n"
            
            # 添加历史对话上下文
            if history:
                prompt += "历史对话：\n"
                for msg in history[-5:]:  # 只使用最近5轮对话
                    prompt += f"{msg['role']}: {msg['content']}\n"
                prompt += "\n"
                
            # 添加额外上下文
            if context:
                prompt += f"额外信息：{context}\n\n"
                
            # 添加当前问题
            prompt += f"问题：{question}\n\n"
            prompt += "请给出详细、准确的回答。如果问题涉及多个方面，请分点说明。"
            
            # 获取回答
            response = self.model.generate_response(prompt)
            print("response:",response)
            
            if not response:
                return "抱歉，我现在无法回答这个问题。请稍后再试。"
            
            # 更新对话历史
            history.append({
                "role": "user",
                "content": question
            })
            history.append({
                "role": "assistant",
                "content": response
            })
            
            # 保持历史记录在合理范围内
            if len(history) > 10:  # 保留最近10轮对话
                history = history[-10:]
                
            self.conversation_contexts[user_id] = history
            
            return response
            
        except Exception as e:
            print(f"Error in answer_question: {str(e)}")
            return "抱歉，系统出现错误，请稍后再试。"

    def clear_conversation_history(self, user_id: str) -> None:
        """清空指定用户的对话历史"""
        if user_id in self.conversation_contexts:
            del self.conversation_contexts[user_id]

    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """获取指定用户的对话历史"""
        return self.conversation_contexts.get(user_id, [])

    def analyze_question(self, question: str) -> Dict:
        """
        分析问题类型和意图
        
        Returns:
            Dict: 包含问题类型、关键词等信息
        """
        prompt = f"""请分析以下问题的类型和意图：
        问题：{question}

        请以JSON格式返回分析结果，包含以下字段：
        - type: 问题类型（如：概念解释、计算题、应用题等）
        - keywords: 关键词列表
        - difficulty: 难度等级（1-5）
        - subject: 可能涉及的学科
        """
        response = self.model.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "type": "unknown",
                "keywords": [],
                "difficulty": 3,
                "subject": "unknown"
            }

    def generate_follow_up_questions(self, question: str, answer: str) -> List[str]:
        """
        生成后续问题建议
        
        Returns:
            List[str]: 建议的后续问题列表
        """
        prompt = f"""基于以下问答，生成3个相关的后续问题：
        问题：{question}
        回答：{answer}

        请以JSON格式返回问题列表。
        """
        response = self.model.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return []

    def evaluate_homework(self, homework: str, answer: str) -> Dict[str, Any]:
        """
        批改作业
        Args:
            homework: 作业内容
            answer: 学生答案
        Returns:
            批改结果
        """
        prompt = f"""请作为一位老师，对以下作业进行批改和评分：
        作业要求：
        {homework}

        学生答案：
        {answer}

        请给出：
        1. 评分（满分100分）
        2. 优点
        3. 需要改进的地方
        4. 具体建议

        请以JSON格式返回，包含以下字段：
        - score: 分数
        - strengths: 优点列表
        - weaknesses: 需要改进的地方列表
        - suggestions: 具体建议列表
        """
        response = self.model.generate_response(prompt)
        result = parse_json_response(response)
        
        # 验证响应是否包含所需字段
        required_fields = ['score', 'strengths', 'weaknesses', 'suggestions']
        if not validate_response(result, required_fields):
            # 如果解析失败，返回默认值
            return {
                "score": 0,
                "strengths": ["无法解析AI响应"],
                "weaknesses": ["请重试"],
                "suggestions": ["请确保作业内容和答案格式正确"]
            }
        
        return result

    def generate_learning_path(self, subject: str, level: str) -> Dict[str, Any]:
        """
        生成学习路径
        Args:
            subject: 学科
            level: 水平
        Returns:
            学习路径
        """
        prompt = f"""请为{level}水平的学生生成{subject}的学习路径。
        请包含以下内容：
        1. 学习目标
        2. 学习内容
        3. 学习顺序
        4. 每个阶段的学习建议

        请以JSON格式返回，包含以下字段：
        - goals: 学习目标列表
        - content: 学习内容列表
        - order: 学习顺序列表
        - suggestions: 学习建议列表
        """
        response = self.model.generate_response(prompt)
        result = parse_json_response(response)
        
        # 验证响应是否包含所需字段
        required_fields = ['goals', 'content', 'order', 'suggestions']
        if not validate_response(result, required_fields):
            # 如果解析失败，返回默认值
            return {
                "goals": ["无法生成学习目标"],
                "content": ["请重试"],
                "order": ["请确保学科和水平信息正确"],
                "suggestions": ["请稍后重试"]
            }
        
        return result

    def analyze_learning_progress(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析学习进度
        Args:
            student_data: 学生学习数据
        Returns:
            分析结果
        """
        prompt = f"""请分析以下学生的学习数据，给出学习进度分析和建议：
        学习数据：
        {student_data}

        请给出：
        1. 总体学习进度（0-100的数值）
        2. 优势领域
        3. 需要加强的领域
        4. 具体建议

        请以JSON格式返回，包含以下字段：
        - overall_progress: 总体进度（0-100的数值）
        - strengths: 优势领域列表
        - weaknesses: 需要加强的领域列表
        - suggestions: 具体建议列表
        """
        response = self.model.generate_response(prompt)
        result = parse_json_response(response)
        
        # 验证响应是否包含所需字段
        required_fields = ['overall_progress', 'strengths', 'weaknesses', 'suggestions']
        if not validate_response(result, required_fields):
            # 如果解析失败，返回默认值
            return {
                "overall_progress": 0,
                "strengths": ["无法分析学习数据"],
                "weaknesses": ["请确保数据格式正确"],
                "suggestions": ["请稍后重试"]
            }
        
        # 确保overall_progress是0-100之间的数值
        try:
            result['overall_progress'] = float(result['overall_progress'])
            result['overall_progress'] = max(0, min(100, result['overall_progress']))
        except (ValueError, TypeError):
            result['overall_progress'] = 0
        
        return result

    def generate_structured_response(self, prompt: str) -> Dict[str, Any]:
        """
        生成结构化的JSON响应
        """
        try:
            # 在提示词中强调返回JSON格式
            structured_prompt = f"{prompt}\n请严格按照JSON格式返回结果。"
            
            # 获取模型响应
            response = self.model.generate_response(structured_prompt)
            
            # 尝试解析JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # 如果解析失败，返回一个基础结构
                print(f"JSON解析失败，原始响应：{response}")
                return {"recommendations": []}
                
        except Exception as e:
            print(f"生成结构化响应时出错: {str(e)}")
            return {"recommendations": []}

    def generate_response(self, prompt: str) -> str:
        """
        生成普通文本响应
        """
        try:
            return self.model.generate_response(prompt)
        except Exception as e:
            print(f"生成响应时出错: {str(e)}")
            return "分析生成失败"

# 创建全局实例
model_service = ModelService() 