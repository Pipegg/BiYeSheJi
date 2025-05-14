# =====================
# 依赖导入
# =====================
from django.db import models
from core import DB

# =====================
# 字段选项
# =====================
XINGBIE_CHOICES = (
    ('男', '男'),
    ('女', '女'),
)

# =====================
# 管理员模型
# =====================
class Admins(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('帐号', max_length=50, default='')
    pwd = models.CharField('密码', max_length=128, default='')
    xingming = models.CharField('姓名', max_length=50, default='')
    xingbie = models.CharField('性别', choices=XINGBIE_CHOICES, max_length=2, default='')
    lianxifangshi = models.CharField('联系方式', max_length=50, default='')
    touxiang = models.CharField('头像', max_length=255, default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'admins'
        verbose_name = '管理员'
        verbose_name_plural = verbose_name





