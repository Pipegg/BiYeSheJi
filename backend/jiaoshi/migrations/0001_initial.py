# Generated by Django 3.2.24 on 2025-05-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jiaoshi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gonghao', models.CharField(default='', max_length=50, verbose_name='工号')),
                ('mima', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('xingming', models.CharField(default='', max_length=50, verbose_name='姓名')),
                ('xingbie', models.CharField(choices=[('男', '男'), ('女', '女')], default='', max_length=512, verbose_name='性别')),
                ('zhicheng', models.CharField(default='', max_length=50, verbose_name='职称')),
                ('lianxifangshi', models.CharField(default='', max_length=50, verbose_name='联系方式')),
                ('youxiang', models.CharField(default='', max_length=50, verbose_name='邮箱')),
                ('touxiang', models.CharField(default='', max_length=255, verbose_name='头像')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
                'db_table': 'jiaoshi',
            },
        ),
    ]
