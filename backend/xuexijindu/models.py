from django.db import models
from core import DB
# Create your models here.
 


class Xuexijindu(models.Model):
    kechengxuexiid = models.IntegerField('课程学习id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    xuexibianhao = models.CharField('学习编号' , max_length = 50,default='') 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    xueshengyonghu = models.CharField('学生用户' ,db_column='xueshengyonghu' , max_length=50,default='') 
    xuexijindu = models.IntegerField('学习进度',default=0)  
    addtime = models.DateTimeField('更新时间' , auto_now_add=True) 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xuexijindu'
        verbose_name = '学习进度'
        verbose_name_plural = verbose_name





