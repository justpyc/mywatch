# Generated by Django 4.1.3 on 2023-05-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('username', models.CharField(max_length=64, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('mobile', models.CharField(max_length=30, verbose_name='手机号')),
                ('rule', models.IntegerField(choices=[(0, '管理员'), (1, '用户')], default=0, verbose_name='权限')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
