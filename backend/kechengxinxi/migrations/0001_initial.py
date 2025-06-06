# Generated by Django 3.2.24 on 2025-05-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kechengxinxi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kechengbianhao', models.CharField(default='', max_length=50, verbose_name='课程编号')),
                ('kechengmingcheng', models.CharField(default='', max_length=255, verbose_name='课程名称')),
                ('kechengfenlei', models.IntegerField(default=0, verbose_name='课程分类')),
                ('kechengfengmian', models.CharField(default='', max_length=255, verbose_name='课程封面')),
                ('kechengyaodian', models.CharField(default='', max_length=50, verbose_name='课程要点')),
                ('fabujiaoshi', models.CharField(db_column='fabujiaoshi', default='', max_length=50, verbose_name='发布教师')),
                ('kechengxiangqing', models.TextField(default='', verbose_name='课程详情')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('issh', models.CharField(default='否', max_length=10, verbose_name='是否审核')),
            ],
            options={
                'verbose_name': '课程信息',
                'verbose_name_plural': '课程信息',
                'db_table': 'kechengxinxi',
            },
        ),
    ]
