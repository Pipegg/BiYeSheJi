from django.db import models
from core import DB
# Create your models here.


class Youqinglianjie(models.Model):
    wangzhanmingcheng = models.CharField('网站名称' , max_length = 50,default='') 
    wangzhi = models.CharField('网址' , max_length = 50,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'youqinglianjie'
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name





