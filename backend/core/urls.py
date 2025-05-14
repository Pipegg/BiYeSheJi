"""
mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include

urlpatterns = [
    path('' , include('common.urls')),
    path('admins/' , include('admins.urls')),
    path('xuesheng/' , include('xuesheng.urls')),
    path('youqinglianjie/' , include('youqinglianjie.urls')),
    path('lunbotu/' , include('lunbotu.urls')),
    path('shoucang/' , include('shoucang.urls')),
    path('siliao/' , include('siliao.urls')),
    path('xiaoxi/' , include('xiaoxi.urls')),
    path('api/xiaoxi/' , include('xiaoxi.urls')),
    path('luntanjiaoliu/' , include('luntanjiaoliu.urls')),
    path('luntanfenlei/' , include('luntanfenlei.urls')),
    path('jiaoliuhuifu/' , include('jiaoliuhuifu.urls')),
    path('jiaoshi/' , include('jiaoshi.urls')),
    path('kechengfenlei/' , include('kechengfenlei.urls')),
    path('kechengxinxi/' , include('kechengxinxi.urls')),
    path('kechengshipin/' , include('kechengshipin.urls')),
    path('kechengziyuan/' , include('kechengziyuan.urls')),
    path('kechengxuexi/' , include('kechengxuexi.urls')),
    path('xuexijindu/' , include('xuexijindu.urls')),
    path('xuexijilu/' , include('xuexijilu.urls')),
    path('buzhizuoye/' , include('buzhizuoye.urls')),
    path('tijiaozuoye/' , include('tijiaozuoye.urls')),
    path('zuoyepiyue/' , include('zuoyepiyue.urls')),
    path('wenda/' , include('wenda.urls')),
    path('huida/' , include('huida.urls')),
    path('wendaxiaoxi/' , include('wendaxiaoxi.urls')),
    path('api/chat/' , include('chat.urls')),
    path('chatbot/' , include('chatbot.urls')),
    path('api/ai/' , include('ai_service.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
