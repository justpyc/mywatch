# Generated by Django 4.2 on 2023-05-07 11:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('watch_app', '0003_uploadrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrecord',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='上传时间'),
            preserve_default=False,
        ),
    ]
