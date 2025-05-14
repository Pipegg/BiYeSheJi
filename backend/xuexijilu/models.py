from django.db import models
from core import DB
# Create your models here.
 


class Xuexijilu(models.Model):
    kechengshipinid = models.IntegerField('课程视频id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    shipinmingcheng = models.CharField('视频名称' , max_length = 255,default='') 
    xueshengyonghu = models.CharField('学生用户' ,db_column='xueshengyonghu' , max_length=50,default='') 
    addtime = models.DateTimeField('学习时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xuexijilu'
        verbose_name = '学习记录'
        verbose_name_plural = verbose_name





