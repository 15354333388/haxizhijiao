# coding: utf-8
# date: 2018-12-28 9:53
# data fields,

# basic response
data = {
    'status': 'OK',
    'msg': '',
    'data': []
}

# user_table fields
user_fields = [
    'u_id',
    'u_sex',
    'u_head_portrait',
    'u_age',
    'u_pwd',
    'u_name',
    'u_pid',
    'u_section',
    'u_group',
    'u_trainlist',
    'u_joblist',
    'u_adress',
    'u_jobwill',
    'u_skill',
    'u_forbid',
    'u_createtime',
    'u_changetime',
    'u_permission'
]

# manoeuvre_table fields
manoeuvre_fields = [
    'y_id',
    'y_name',
    'y_content',
    'y_creator',
    'y_createtime',
    'y_changetime',
    'y_receive',
    'y_finished',
    'y_endtime',
]

# manoeuvre_middle_table fields
manoeuvre_middle_fields = [
    'ym_id',
    'ym_manoeuvre',
    'ym_user',
    'ym_video_url',
    'ym_image_url',
    'ym_answer ',
    'ym_score',
    'ym_timeremaining',
    'ym_result',
    'ym_createtime',
    'ym_changetime',
    'ym_finished',
    'ym_finishedtime'
]

# train_table fields
train_fields =[
    't_id',
    't_name',
    't_content',
    't_createtime',
    't_changetime',
    't_receive',
    't_endtime',
]

# train_middle fields
train_middle_fields = [
    'tm_id',
    'tm_user',
    'tm_train',
    'tm_result',
    'tm_timeremaining',
    'tm_createtime',
    'tm_changetime',
    'tm_finished',
    'tm_finishedtime',
    'tm_score'
]

# examine_table_fields
examine_fields = [
    'e_id',
    'e_name',
    'e_content',
    'e_createtime',
    'e_changetime',
    'e_receive',
    'e_endtime',
]

# examine_middle fields
examine_middle_fields = [
    'em_id',
    'em_user',
    'em_examine',
    'em_result',
    'em_timeremaining',
    'em_createtime',
    'em_changetime',
    'em_score',
    'em_finished',
    'em_unfinished',
]

# work_table_fields
work_fields = [
    'w_id',
    'w_name',
    'w_content',
    'w_createtime',
    'w_changetime',
    'w_receive',
    'w_endtime',
]

# work_middle fields
work_middle_fields = [
    'wm_id',
    'wm_user',
    'wm_work',
    'wm_result',
    'wm_timeremaining',
    'wm_createtime',
    'wm_changetime',
    'wm_score',
    'wm_finished',
    'wm_finishedtime',
]

# bank fields
bank_fields = [
    'b_id',
    'b_content',
    'b_choiceA',
    'b_choiceB',
    'b_choiceC',
    'b_choiceD',
    'b_true',
    'b_createtime',
    'b_changetime',
]

# finished incident table
incident_fields = [
    'i_id',
    'i_table',
    'i_symbol',
    'i_createtime',
    'i_endtime',
    'i_finished',
]

message_fields = [
    'm_id',
    'm_send',
    'm_type',
    'm_receive',
    'm_symbol',
    'm_createtime',
    'm_is_send',
]

chat_fields = [
    'c_id',
    'c_send',
    'c_receive',
    'c_content',
    'c_createtime',
    'c_is_send',
]
# # unfinished incident table
# unfinished_incident_fields = [
#     'ui_id',
#     'ui_table',
#     'ui_symbol',
# ]