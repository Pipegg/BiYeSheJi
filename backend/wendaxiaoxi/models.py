from django.db import models
from core import DB
# Create your models here.
 


class Wendaxiaoxi(models.Model):
    xiaoxineirong = models.TextField('消息内容',default='') 
    huifuneirong = models.TextField('回复内容',default='') 
    guanlianhuifu = models.IntegerField('关联回复',default=0) 
    yonghu = models.CharField('用户' ,db_column='yonghu' , max_length=50,default='') 
    addtime = models.DateTimeField('添加时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'wendaxiaoxi'
        verbose_name = '问答消息'
        verbose_name_plural = verbose_name





