from django.db import models
from core import DB
# Create your models here.
XINGBIE_CHOICES = (
   ('男' , '男') , 
   ('女' , '女') , 

    )  


class Xuesheng(models.Model):
    xuehao = models.CharField('学号' , max_length = 50,default='') 
    mima = models.CharField('密码' , max_length = 128,default='') 
    xingming = models.CharField('姓名' , max_length = 50,default='') 
    xingbie = models.CharField('性别' , choices=XINGBIE_CHOICES , max_length=512,default='') 
    shouji = models.CharField('手机' , max_length = 50,default='') 
    youxiang = models.CharField('邮箱' , max_length = 50,default='')
    touxiang = models.CharField('头像',max_length=255,default='') 
    issh = models.CharField('是否审核' , max_length = 10 , default='否')




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'xuesheng'
        verbose_name = '学生'
        verbose_name_plural = verbose_name





