from django.db import models
from core import DB
# Create your models here.
 


class Jiaoliuhuifu(models.Model):
    luntanjiaoliuid = models.IntegerField('论坛交流id',default=0)  
    bianhao = models.CharField('编号' , max_length = 50,default='') 
    biaoti = models.CharField('标题' , max_length = 50,default='') 
    fenlei = models.IntegerField('分类',default=0) 
    faburen = models.CharField('发布人' ,db_column='faburen' , max_length=50,default='') 
    jiaoliuneirong = models.TextField('交流内容',default='' ) 
    huifuren = models.CharField('回复人' ,db_column='huifuren' , max_length=50,default='') 
    huifuquanxian = models.CharField('回复权限' , max_length = 50,default='') 
    touxiang = models.CharField('头像',max_length=255,default='') 
    xingming = models.CharField('姓名' , max_length = 50,default='') 
    addtime = models.DateTimeField('回复时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'jiaoliuhuifu'
        verbose_name = '交流回复'
        verbose_name_plural = verbose_name





