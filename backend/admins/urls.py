from django.urls import path,include
from .views import router

# 路由注册
urlpatterns = router.urls
