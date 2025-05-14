from django.db import models
from core import DB
from django.contrib.auth.models import User
# Create your models here.
 


class Tijiaozuoye(models.Model):
    buzhizuoyeid = models.IntegerField('布置作业id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    zuoyebianhao = models.CharField('作业编号' , max_length = 50,default='') 
    zuoyemingcheng = models.CharField('作业名称' , max_length = 255,default='') 
    zuoyefujian = models.CharField('作业附件',max_length=255,default='') 
    xueshengxingming = models.CharField('学生姓名' , max_length = 50,default='') 
    zuoyezhuangtai = models.CharField('作业状态' , max_length = 50,default='') 
    tijiaoxuesheng = models.CharField('提交学生' ,db_column='tijiaoxuesheng' , max_length=50,default='') 
    addtime = models.DateTimeField('提交时间' , auto_now_add=True) 

    def _get_ZuoyepiyueCount(self):
        return DB.name("zuoyepiyue").where("tijiaozuoyeid" , self.id).count()
    zuoyepiyueCount = property(_get_ZuoyepiyueCount)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'tijiaozuoye'
        verbose_name = '提交作业'
        verbose_name_plural = verbose_name

class Homework(models.Model):
    title = models.CharField('作业标题', max_length=255)
    content = models.TextField('作业内容')
    type = models.CharField('作业类型', max_length=50, default='homework')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    due_date = models.DateTimeField('截止日期', null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_homework')
    course = models.ForeignKey('kechengxuexi.Course', on_delete=models.CASCADE, related_name='homework')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'homework'
        verbose_name = '作业'
        verbose_name_plural = verbose_name

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_submissions')
    answer = models.TextField('答案')
    score = models.FloatField('分数', null=True, blank=True)
    feedback = models.TextField('反馈', null=True, blank=True)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.homework.title}"

    class Meta:
        db_table = 'homework_submission'
        verbose_name = '作业提交'
        verbose_name_plural = verbose_name





