from django.db import models
from core import DB
# Create your models here.


class Shoucang(models.Model):
    username = models.CharField('用户' ,db_column='username' , max_length=50,default='') 
    xwid = models.IntegerField('关联表id',default=0)  
    biao = models.CharField('关联表' , max_length = 50,default='') 
    biaoti = models.CharField('标题' , max_length = 255,default='') 
    addtime = models.DateTimeField('收藏时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'shoucang'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name





