from django.db import models
from core import DB
# Create your models here.
JIANSUOLEIXING_CHOICES = (
   ('精准' , '精准') , 
   ('模糊' , '模糊') , 

    )  


class Wenda(models.Model):
    tiwenneirong = models.CharField('提问内容' , max_length = 255,default='') 
    jiansuoleixing = models.CharField('检索类型' , choices=JIANSUOLEIXING_CHOICES , max_length=512,default='') 




    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'wenda'
        verbose_name = '问答'
        verbose_name_plural = verbose_name





