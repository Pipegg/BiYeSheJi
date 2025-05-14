from django.db import models
from core import DB
# Create your models here.
 


class Kechengxinxi(models.Model):
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    kechengfengmian = models.CharField('课程封面',max_length=255,default='') 
    kechengyaodian = models.CharField('课程要点' , max_length = 50,default='') 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    kechengxiangqing = models.TextField('课程详情',default='' ) 
    addtime = models.DateTimeField('发布时间' , auto_now_add=True) 
    issh = models.CharField('是否审核' , max_length = 10 , default='否')

    def _get_KechengshipinCount(self):
        return DB.name("kechengshipin").where("kechengxinxiid" , self.id).count()
    kechengshipinCount = property(_get_KechengshipinCount)
    def _get_KechengziyuanCount(self):
        return DB.name("kechengziyuan").where("kechengxinxiid" , self.id).count()
    kechengziyuanCount = property(_get_KechengziyuanCount)
    def _get_KechengxuexiCount(self):
        return DB.name("kechengxuexi").where("kechengxinxiid" , self.id).count()
    kechengxuexiCount = property(_get_KechengxuexiCount)
    def _get_BuzhizuoyeCount(self):
        return DB.name("buzhizuoye").where("kechengxinxiid" , self.id).count()
    buzhizuoyeCount = property(_get_BuzhizuoyeCount)



    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'kechengxinxi'
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name





