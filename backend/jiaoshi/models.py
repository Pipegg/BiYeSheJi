from django.db import models
from core import DB
# Create your models here.
XINGBIE_CHOICES = (
   ('男' , '男') , 
   ('女' , '女') , 

    )  


class Jiaoshi(models.Model):
    gonghao = models.CharField('工号' , max_length = 50,default='') 
    mima = models.CharField('密码' , max_length = 128,default='') 
    xingming = models.CharField('姓名' , max_length = 50,default='') 
    xingbie = models.CharField('性别' , choices=XINGBIE_CHOICES , max_length=512,default='') 
    zhicheng = models.CharField('职称' , max_length = 50,default='') 
    lianxifangshi = models.CharField('联系方式' , max_length = 50,default='') 
    youxiang = models.CharField('邮箱' , max_length = 50,default='') 
    touxiang = models.CharField('头像',max_length=255,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'jiaoshi'
        verbose_name = '教师'
        verbose_name_plural = verbose_name





