from django.db import models
from core import DB
# Create your models here.
 


class Zuoyepiyue(models.Model):
    tijiaozuoyeid = models.IntegerField('提交作业id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    zuoyemingcheng = models.CharField('作业名称' , max_length = 255,default='') 
    zuoyefujian = models.CharField('作业附件',max_length=255,default='') 
    xueshengxingming = models.CharField('学生姓名' , max_length = 50,default='') 
    tijiaoxuesheng = models.CharField('提交学生' ,db_column='tijiaoxuesheng' , max_length=50,default='') 
    fenshu = models.IntegerField('分数',default=0)  
    pingyu = models.TextField('评语',default='') 
    addtime = models.DateTimeField('批阅时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'zuoyepiyue'
        verbose_name = '作业批阅'
        verbose_name_plural = verbose_name





