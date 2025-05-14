from django.db import models
from core import DB
# Create your models here.
 


class Kechengziyuan(models.Model):
    kechengxinxiid = models.IntegerField('课程信息id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    ziyuanmingcheng = models.CharField('资源名称' , max_length = 255,default='') 
    ziyuanfujian = models.CharField('资源附件',max_length=255,default='') 
    ziyuanshuoming = models.TextField('资源说明',default='' ) 
    addtime = models.DateTimeField('发布时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'kechengziyuan'
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name





