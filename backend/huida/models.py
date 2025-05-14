from django.db import models
from core import DB
# Create your models here.
 


class Huida(models.Model):
    wenti = models.IntegerField('问题',default=0) 
    huidaneirong = models.TextField('回答内容',default='') 
    quanzhi = models.IntegerField('权值',default=0)  
    huidacishu = models.IntegerField('回答次数',default=0)  




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'huida'
        verbose_name = '回答'
        verbose_name_plural = verbose_name





