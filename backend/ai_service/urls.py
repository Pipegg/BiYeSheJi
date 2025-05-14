# =====================
# 依赖导入
# =====================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AIConversationViewSet,
    AIHomeworkEvaluationViewSet,
    AILearningPathViewSet,
    AILearningAnalysisViewSet
)

# =====================
# 路由注册
# =====================
router = DefaultRouter()
router.register(r'conversation', AIConversationViewSet, basename='conversation')
router.register(r'homework-evaluation', AIHomeworkEvaluationViewSet, basename='homework-evaluation')
router.register(r'learning-path', AILearningPathViewSet, basename='learning-path')
router.register(r'learning-analysis', AILearningAnalysisViewSet, basename='learning-analysis')

# =====================
# URL Patterns
# =====================
urlpatterns = [
    path('', include(router.urls)),  # 包含所有AI服务相关接口
] 