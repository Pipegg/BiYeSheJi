# =====================
# 依赖导入
# =====================
from django.urls import path
from . import views

# =====================
# URL配置
urlpatterns = [
    path('admin/selectAll/', views.selectAll),
    path('admin/list/', views.adminlist),
    path('admin/fabujiaoshi/', views.fabujiaoshi),
    path('/findById/', views.findById),
    path('detail/', views.detail),
    path('delete/', views.delete),
    path('insert/', views.insert),
    path('update/', views.update),
]
