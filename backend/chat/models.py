from django.db import models

# Create your models here.

class ChatHistory(models.Model):
    """对话历史记录"""
    user_id = models.CharField(max_length=50, verbose_name='用户ID')
    question = models.TextField(verbose_name='问题')
    answer = models.TextField(verbose_name='回答')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'chat_history'
        verbose_name = '对话历史'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user_id} - {self.created_at}'
