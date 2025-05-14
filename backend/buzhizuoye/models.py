from django.db import models
from core import DB
from typing import Any
# Create your models here.
 

# 布置作业模型
class Buzhizuoye(models.Model):
    """
    布置作业模型
    用于存储教师布置的作业信息
    """
    kechengxinxiid = models.IntegerField(verbose_name='课程信息ID')
    kechengbianhao = models.CharField(max_length=50, verbose_name='课程编号')
    kechengmingcheng = models.CharField(max_length=50, verbose_name='课程名称')
    kechengfenlei = models.IntegerField(verbose_name='课程分类')
    fabujiaoshi = models.CharField(max_length=50, verbose_name='发布教师')
    zuoyebianhao = models.CharField(max_length=50, verbose_name='作业编号')
    jiezhiriqi = models.CharField(max_length=50, verbose_name='截止日期')
    zuoyemingcheng = models.CharField(max_length=50, verbose_name='作业名称')
    zuoyefujian = models.CharField(max_length=255, verbose_name='作业附件')
    yitijiaorenshu = models.IntegerField(verbose_name='已提交人数')
    zuoyemiaoshu = models.TextField(verbose_name='作业描述')

    def _get_TijiaozuoyeCount(self) -> int:
        """获取已提交作业数量"""
        from tijiaozuoye.models import Tijiaozuoye
        return Tijiaozuoye.objects.filter(buzhizuoyeid=self.pk).count()
    tijiaozuoyeCount = property(_get_TijiaozuoyeCount)



    def __str__(self) -> str:
        """返回作业名称作为字符串表示"""
        return self.zuoyemingcheng

    class Meta:
        db_table = 'buzhizuoye'
        verbose_name = '布置作业'
        verbose_name_plural = verbose_name





