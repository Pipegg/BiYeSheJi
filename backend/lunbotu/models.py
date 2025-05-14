from django.db import models
from core import DB
# Create your models here.


class Lunbotu(models.Model):
    title = models.CharField('标题' , max_length = 50,default='') 
    image = models.CharField('图片',max_length=255,default='') 
    url = models.CharField('连接地址' , max_length = 255,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'lunbotu'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name





