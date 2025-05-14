from django.db import models
from core import DB
# Create your models here.
 


class Kechengshipin(models.Model):
    kechengxinxiid = models.IntegerField('课程信息id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    shipinmingcheng = models.CharField('视频名称' , max_length = 255,default='') 
    shipin = models.CharField('视频',max_length=255,default='') 
    xuexicishu = models.IntegerField('学习次数',default=0)  
    shipinjieshao = models.TextField('视频介绍',default='' ) 
    addtime = models.DateTimeField('发布时间' , auto_now_add=True) 

    def _get_XuexijiluCount(self):
        return DB.name("xuexijilu").where("kechengshipinid" , self.id).count()
    xuexijiluCount = property(_get_XuexijiluCount)



    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'kechengshipin'
        verbose_name = '课程视频'
        verbose_name_plural = verbose_name





