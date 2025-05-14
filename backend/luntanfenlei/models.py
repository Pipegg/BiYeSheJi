from django.db import models
from core import DB
# Create your models here.


class Luntanfenlei(models.Model):
    fenleimingcheng = models.CharField('分类名称' , max_length = 255,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'luntanfenlei'
        verbose_name = '论坛分类'
        verbose_name_plural = verbose_name





