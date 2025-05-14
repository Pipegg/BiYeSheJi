from django.db import models
from core import DB
# Create your models here.


class Siliao(models.Model):
    bianhao = models.CharField('编号' , max_length = 50,default='') 
    shouxinren = models.CharField('收信人' ,db_column='shouxinren' , max_length=50,default='') 
    faxinren = models.CharField('发信人' ,db_column='faxinren' , max_length=50,default='') 
    addtime = models.DateTimeField('消息最后时间' , auto_now_add=True) 

    def _get_XiaoxiCount(self):
        return DB.name("xiaoxi").where("siliaoid" , self.id).count()
    xiaoxiCount = property(_get_XiaoxiCount)



    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'siliao'
        verbose_name = '私聊'
        verbose_name_plural = verbose_name





