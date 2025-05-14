# =====================
# 依赖导入
# =====================
from django.db import models
from django.contrib.auth import get_user_model

# =====================
# 用户模型
# =====================
User = get_user_model()

# =====================
# 业务模型定义
# =====================
class AIConversation(models.Model):
    """AI对话记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    question = models.TextField()
    answer = models.TextField()
    context = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class AIHomeworkEvaluation(models.Model):
    """AI作业批改记录"""
    homework = models.ForeignKey('tijiaozuoye.Tijiaozuoye', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    strengths = models.JSONField()
    weaknesses = models.JSONField()
    suggestions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class AILearningPath(models.Model):
    """AI生成的学习路径"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    goals = models.JSONField()
    content = models.JSONField()
    order = models.JSONField()
    suggestions = models.JSONField()
    progress = models.JSONField(default=list, verbose_name='阶段进度')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class AILearningAnalysis(models.Model):
    """AI学习进度分析"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    overall_progress = models.FloatField()
    strengths = models.JSONField()
    weaknesses = models.JSONField()
    suggestions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] 