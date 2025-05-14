from django.db import models
from core import DB
from django.contrib.auth.models import User

# Create your models here.
 
XUEXIZHUANGTAI_CHOICES = (
   ('待学习' , '待学习') , 
   ('学习中' , '学习中') , 
   ('已完成' , '已完成') , 
)

class Course(models.Model):
    title = models.CharField('课程名称', max_length=255)
    code = models.CharField('课程编号', max_length=50, unique=True)
    description = models.TextField('课程描述')
    category = models.IntegerField('课程分类', default=0)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_courses')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name

class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    progress = models.IntegerField('学习进度', default=0)
    status = models.CharField('学习状态', choices=XUEXIZHUANGTAI_CHOICES, max_length=50, default='待学习')
    last_accessed = models.DateTimeField('最后访问时间', auto_now=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    class Meta:
        db_table = 'course_progress'
        verbose_name = '课程进度'
        verbose_name_plural = verbose_name
        unique_together = ('course', 'student')

class Kechengxuexi(models.Model):
    kechengxinxiid = models.IntegerField('课程信息id',default=0)  
    kechengbianhao = models.CharField('课程编号' , max_length = 50,default='') 
    kechengmingcheng = models.CharField('课程名称' , max_length = 255,default='') 
    kechengfenlei = models.IntegerField('课程分类',default=0) 
    fabujiaoshi = models.CharField('发布教师' ,db_column='fabujiaoshi' , max_length=50,default='') 
    xuexibianhao = models.CharField('学习编号' , max_length = 50,default='') 
    xuexijindu = models.IntegerField('学习进度',default=0)  
    xueshengyonghu = models.CharField('学生用户' ,db_column='xueshengyonghu' , max_length=50,default='') 
    xuexizhuangtai = models.CharField('学习状态' , choices=XUEXIZHUANGTAI_CHOICES , max_length=512,default='') 
    addtime = models.DateTimeField('学习时间' , auto_now_add=True) 

    def _get_XuexijinduCount(self):
        return DB.name("xuexijindu").where("kechengxuexiid" , self.id).count()
    xuexijinduCount = property(_get_XuexijinduCount)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'kechengxuexi'
        verbose_name = '课程学习'
        verbose_name_plural = verbose_name





