from django.db import models

gender_choices = (
    (0, '男'),
    (1, '女'),
)

rule_choices = (
    (0, '管理员'),
    (1, '用户'),
)

analysis_choices = (
    (0, '分析中'),
    (1, '完成'),
)

class User(models.Model):

    id = models.AutoField(primary_key=True,verbose_name="用户ID")
    username = models.CharField(max_length=64, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    gender = models.IntegerField(choices=gender_choices, default=0, verbose_name="性别")
    mobile = models.CharField(max_length=30, verbose_name='手机号')
    rule = models.IntegerField(choices=rule_choices, default=1, verbose_name="权限")


    class Meta:
        db_table = 'user'


class AnalysisRecord(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name="任务ID")
    upload_id = models.IntegerField(verbose_name='文件ID')
    uid = models.IntegerField(verbose_name='用户ID')
    pictures = models.TextField(verbose_name='图片列表') # "逗号分开"
    status = models.IntegerField(choices=analysis_choices, default=0, verbose_name="任务状态")

    class Meta:
        db_table = 'analysis_record'


class UploadRecord(models.Model):
    """
    文件上传记录
    """
    id = models.AutoField(primary_key=True,verbose_name="序列ID")
    uid = models.IntegerField(verbose_name='用户ID')
    location = models.CharField(max_length=256, verbose_name="文件路径")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    
    class Meta:
        db_table = 'upload_record'


