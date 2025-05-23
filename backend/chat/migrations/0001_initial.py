# Generated by Django 3.2.24 on 2025-05-06 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, verbose_name='用户ID')),
                ('question', models.TextField(verbose_name='问题')),
                ('answer', models.TextField(verbose_name='回答')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '对话历史',
                'verbose_name_plural': '对话历史',
                'db_table': 'chat_history',
                'ordering': ['-created_at'],
            },
        ),
    ]
