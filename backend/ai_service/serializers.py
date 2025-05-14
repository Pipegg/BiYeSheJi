# =====================
# 依赖导入
# =====================
from rest_framework import serializers
from .models import (
    AIConversation,
    AIHomeworkEvaluation,
    AILearningPath,
    AILearningAnalysis
)

# =====================
# 序列化器定义
# =====================
class AIConversationSerializer(serializers.ModelSerializer):
    """AI对话记录序列化器"""
    class Meta:
        model = AIConversation
        fields = ['id', 'user', 'question', 'answer', 'context', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class AIHomeworkEvaluationSerializer(serializers.ModelSerializer):
    """AI作业批改记录序列化器"""
    class Meta:
        model = AIHomeworkEvaluation
        fields = ['id', 'homework', 'student', 'score', 'strengths', 'weaknesses', 'suggestions', 'created_at']
        read_only_fields = ['student', 'created_at']

class AILearningPathSerializer(serializers.ModelSerializer):
    """AI学习路径序列化器"""
    class Meta:
        model = AILearningPath
        fields = ['id', 'student', 'subject', 'level', 'goals', 'content', 'order', 'suggestions', 'progress', 'created_at', 'updated_at']
        read_only_fields = ['student', 'created_at', 'updated_at']

class AILearningAnalysisSerializer(serializers.ModelSerializer):
    """AI学习进度分析序列化器"""
    class Meta:
        model = AILearningAnalysis
        fields = ['id', 'student', 'overall_progress', 'strengths', 'weaknesses', 'suggestions', 'created_at']
        read_only_fields = ['student', 'created_at'] 