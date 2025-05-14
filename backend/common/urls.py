from django.urls import path, include
from .views import login, logout, query, mod, upload, captcha, token_login, checkon, filter, xuanlian

# 后端接口路径
urlpatterns = [
    # 登录
    path('login/', login),
    # 退出
    path('logout/', logout),
    # 查询数据
    path('query/', query),
    # 修改操作
    path('mod/', mod),
    # 上传
    path('upload/', upload),
    # 图片验证码
    path('captch/', captcha),
    # Token登录
    path('tokenLogin/', token_login),
    # 检查重复
    path('checkon/', checkon),
    # 过滤
    path('filter/', filter),
    # 训练
    path('xunlian/', xuanlian),
    # 代理API，处理跨域请求
    path('api/proxy/', include('common.proxy_api')),
]





