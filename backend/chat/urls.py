from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask_question, name='ask_question'),
    path('history/', views.get_history, name='get_history'),
    path('clear/', views.clear_history, name='clear_history'),
    path('follow-up/', views.get_follow_up_questions, name='follow_up_questions'),
    path('sessionList/', views.session_list, name='session_list'),
    path('check/', views.check, name='check'),
    path('updateRead/', views.update_read, name='update_read'),
]





