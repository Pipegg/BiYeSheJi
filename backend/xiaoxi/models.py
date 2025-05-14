from django.db import models
from core import DB
# Create your models here.


class Xiaoxi(models.Model):
    siliaoid = models.IntegerField('私聊id',default=0)  
    bianhao = models.CharField('编号' , max_length = 50,default='') 
    neirong = models.TextField('内容',default='' ) 
    fasongren = models.CharField('发送人' ,db_column='fasongren' , max_length=50,default='') 
    fasongshijian = models.CharField('发送时间' , max_length=19,default='' ) 
    shifouzhakan = models.CharField('是否查看' , max_length = 50,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xiaoxi'
        verbose_name = '消息'
        verbose_name_plural = verbose_name





