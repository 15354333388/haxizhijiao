#coding: utf-8
#time: 2018-12-28 10:38
from django.db import models
from time import timezone

# Create your models here.

#user table
sex = (
    ('1', '男'),
    ('2', '女')
)


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=64)
    u_sex = models.CharField(max_length=16, choices=sex)
    u_age = models.CharField(max_length=16)
    u_pwd = models.CharField(max_length=64, null=True, blank=True, unique=True)
    u_pid = models.CharField(max_length=64, unique=True)
    u_section = models.CharField(max_length=32)  # 科室
    u_trainlist = models.CharField(max_length=4096)
    u_joblist = models.CharField(max_length=4096)
    u_home = models.CharField(max_length=255)
    u_jobwill = models.CharField(max_length=4096)
    u_skill = models.CharField(max_length=255)
    u_forbid = models.BooleanField(default=0)
    u_permission = models.CharField(max_length=4, default='3')


finish = (
    (0, '未完成'),
    (1, '完成')
)
# manoeuvre table 演练表格
class Manoeuvre(models.Model):
    y_id = models.AutoField(primary_key=True)
    y_name = models.CharField(max_length=255)
    y_content = models.CharField(max_length=255)
    y_creator = models.CharField(max_length=64)
    y_createtime = models.DateTimeField(auto_now_add=True)
    # y_receive = models.CharField(max_length=255)
    y_endtime = models.IntegerField() # unit is minute


# manoeuvre middle table 演练中间表
class ManoeuverMiddle(models.Model):
    ym_id = models.AutoField(primary_key=True)
    ym_manoeuvre = models.ForeignKey(to =Manoeuvre, on_delete=models.CASCADE, to_field='y_id')
    ym_user = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field='u_id')
    ym_video_url = models.CharField(max_length=256, null=True)
    ym_image_url = models.CharField(max_length=256, null=True)
    ym_answer = models.CharField(max_length=256, null=True)
    ym_score = models.IntegerField(null=True)
    ym_timeremaining = models.IntegerField()
    ym_result = models.CharField(max_length=256, null=True)
    ym_createtime = models.DateTimeField(auto_now_add=True)
    ym_finished = models.BooleanField(choices=finish, default=0)