from django.db import models
from core import DB
# Create your models here.
 


class Luntanjiaoliu(models.Model):
    bianhao = models.CharField('编号' , max_length = 50,default='') 
    biaoti = models.CharField('标题' , max_length = 50,default='') 
    fenlei = models.IntegerField('分类',default=0) 
    tupian = models.CharField('图片',max_length=255,default='') 
    huifushu = models.IntegerField('回复数',default=0)  
    faburen = models.CharField('发布人' ,db_column='faburen' , max_length=50,default='') 
    hudongneirong = models.TextField('互动内容',default='' ) 
    quanxian = models.CharField('权限' , max_length = 50,default='') 
    xingming = models.CharField('姓名' , max_length = 50,default='') 
    touxiang = models.CharField('头像',max_length=255,default='') 
    addtime = models.DateTimeField('发布时间' , auto_now_add=True) 
    issh = models.CharField('是否审核' , max_length = 10 , default='否')

    def _get_JiaoliuhuifuCount(self):
        return DB.name("jiaoliuhuifu").where("luntanjiaoliuid" , self.id).count()
    jiaoliuhuifuCount = property(_get_JiaoliuhuifuCount)



    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'luntanjiaoliu'
        verbose_name = '论坛交流'
        verbose_name_plural = verbose_name





