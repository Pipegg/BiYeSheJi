from django.db import models
from core import DB
# Create your models here.


class Kechengfenlei(models.Model):
    fenleimingcheng = models.CharField('分类名称' , max_length = 255,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'kechengfenlei'
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name





