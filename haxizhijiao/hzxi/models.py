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
    u_head_portrait = models.CharField(max_length=256, default='/static/img/show.jpg')
    u_age = models.CharField(max_length=16)
    u_pwd = models.CharField(max_length=64, null=True, blank=True, unique=True)
    u_pid = models.CharField(max_length=64, unique=True)
    u_group = models.CharField(max_length=64, null=True, blank=True)
    u_section = models.CharField(max_length=32)  # 科室
    u_trainlist = models.CharField(max_length=4096)
    u_joblist = models.CharField(max_length=4096)
    u_adress = models.CharField(max_length=255)
    u_jobwill = models.CharField(max_length=4096)
    u_skill = models.CharField(max_length=255)
    u_forbid = models.BooleanField(default=0)
    u_permission = models.CharField(max_length=4, default='3')
    u_createtime = models.DateTimeField(auto_now_add=True)
    u_changetime = models.DateTimeField(auto_now=True)


# finish = (
#     (0, '未完成'),
#     (1, '完成')
# )
# manoeuvre table 演练表格
class Manoeuvre(models.Model):
    y_id = models.AutoField(primary_key=True)
    y_name = models.CharField(max_length=255)
    y_content = models.CharField(max_length=255)
    y_creator = models.CharField(max_length=64)
    y_createtime = models.DateTimeField(auto_now_add=True)
    y_changetime = models.DateTimeField(auto_now=True)
    y_receive = models.CharField(max_length=255)
    y_finished = models.BooleanField(default=False)
    y_endtime = models.IntegerField(null=True) # unit is minute


# manoeuvre middle table 演练中间表
class ManoeuverMiddle(models.Model):
    ym_id = models.AutoField(primary_key=True)
    ym_manoeuvre = models.ForeignKey(to =Manoeuvre, on_delete=models.CASCADE, to_field='y_id')
    ym_user = models.ForeignKey(to=User, on_delete=models.CASCADE, to_field='u_id')
    ym_video_url = models.CharField(max_length=256, null=True)
    ym_image_url = models.CharField(max_length=256, null=True)
    ym_files_url = models.CharField(max_length=256, null=True)
    ym_answer = models.CharField(max_length=256, null=True)
    ym_score = models.IntegerField(null=True)
    ym_timeremaining = models.IntegerField()
    ym_result = models.CharField(max_length=256, null=True)
    ym_createtime = models.DateTimeField(auto_now_add=True)
    ym_changetime = models.DateTimeField(auto_now=True)
    ym_finished = models.BooleanField(default=False)
    ym_finishedtime = models.DateTimeField(null=True)


# train table 培训
class Train(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=256)
    t_content = models.CharField(max_length=256)
    t_receive = models.CharField(max_length=255)
    t_createtime = models.DateTimeField(auto_now_add=True)
    t_changetime = models.DateTimeField(auto_now=True)
    t_endtime = models.IntegerField()


# record about train and user information
class TrainMiddle(models.Model):
    tm_id = models.AutoField(primary_key=True)
    tm_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tm_train = models.ForeignKey(to=Train, on_delete=models.CASCADE)
    tm_result = models.CharField(max_length=256, null=True)
    tm_timeremaining = models.IntegerField()
    tm_createtime = models.DateTimeField(auto_now_add=True)
    tm_changetime = models.DateTimeField(auto_now=True)
    tm_score = models.IntegerField(null=True)
    tm_finished = models.BooleanField(default=False)
    tm_finishedtime = models.DateTimeField(null=True)


# examine bank table
class Bank(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_content = models.CharField(max_length=256)
    b_choiceA = models.CharField(max_length=256)
    b_choiceB = models.CharField(max_length=256)
    b_choiceC = models.CharField(max_length=256)
    b_choiceD = models.CharField(max_length=256)
    b_true = models.CharField(max_length=4)
    b_createtime = models.DateTimeField(auto_now_add=True)
    b_changetime = models.DateTimeField(auto_now=True)


# examine table 考核
class Examine(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=256)
    e_content = models.CharField(max_length=256)
    e_createtime = models.DateTimeField(auto_now_add=True)
    e_changetime = models.DateTimeField(auto_now=True)
    e_receive = models.CharField(max_length=255)
    e_endtime = models.IntegerField()


# recode about examine and user information
class ExamineMiddle(models.Model):
    em_id = models.AutoField(primary_key=True)
    em_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    em_examine = models.ForeignKey(to=Examine, on_delete=models.CASCADE)
    em_result = models.CharField(max_length=256, null=True)
    em_createtime = models.DateTimeField(auto_now_add=True)
    em_changetime = models.DateTimeField(auto_now=True)
    em_timeremaining = models.IntegerField()
    em_score = models.IntegerField()
    em_finished = models.BooleanField(default=False)
    em_finishedtime = models.DateTimeField(null=True)


# work table
class Work(models.Model):
    w_id = models.AutoField(primary_key=True)
    w_name = models.CharField(max_length=256)
    w_content = models.CharField(max_length=256)
    w_createtime = models.DateTimeField(auto_now_add=True)
    w_changetiem = models.DateTimeField(auto_now=True)
    w_receive = models.CharField(max_length=255)
    w_endtime = models.IntegerField()


# recode about work and user information
class WorkMiddle(models.Model):
    wm_id = models.AutoField(primary_key=True)
    wm_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    wm_work = models.ForeignKey(to=Work, on_delete=models.CASCADE)
    wm_result = models.CharField(max_length=256, null=True)
    wm_createtime = models.DateTimeField(auto_now_add=True)
    wm_changetime = models.DateTimeField(auto_now=True)
    wm_timeremaining = models.IntegerField()
    wm_score = models.IntegerField()
    em_finished = models.BooleanField(default=False)
    em_finishedtime = models.DateTimeField(null=True)


# finished incident table
class Incident(models.Model):
    i_id = models.AutoField(primary_key=True)
    i_table = models.CharField(max_length=64)
    i_symbol = models.IntegerField()
    i_finished = models.BooleanField(default=False)
    i_createtime = models.DateTimeField(auto_now_add=True)
    i_endtime = models.DateTimeField(null=True)
    # fi_createtime = models.DateTimeField(auto_now_add=True)
#
#
# class Userp(models.Model):
#     avatar = models.CharField(max_length=256)


class Message(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_send = models.IntegerField()
    m_type = models.CharField(max_length=64, default='manoeuvre')
    m_receive = models.IntegerField()
    m_symbol = models.IntegerField()
    m_createtime = models.DateTimeField(auto_now_add=True)
    m_is_send = models.BooleanField(default=False)


class Chat(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_send = models.IntegerField()
    c_receive = models.IntegerField()
    c_content = models.CharField(max_length=2048)
    c_createtime = models.DateTimeField(auto_now_add=True)
    c_is_send = models.BooleanField(default=False)


# class OldMessage(models.Model):
#     om_id = models.AutoField(primary_key=True)
#     om_send = models.IntegerField()
#     om_receive = models.IntegerField()
#     om_content = models.CharField(max_length=2048)
#     # om_old = models.CharField(max_length=2048)
#     om_createtime = models.DateTimeField(auto_now_add=True)


class LoginUser(models.Model):
    l_id = models.AutoField(primary_key=True)
    l_u_id = models.IntegerField()
    l_createtime = models.DateTimeField(auto_now_add=True)
    l_changetime = models.DateTimeField(null=True)
    l_islogin = models.BooleanField(default=True)
