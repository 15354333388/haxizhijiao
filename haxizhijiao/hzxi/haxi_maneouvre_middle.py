# coding: utf-8

import os
from django.db import transaction
from . import  models
from . import database_operation
from . import database
from . import haxi_qiniuyun
from . import haxi_file
from haxizhijiao import settings
from .haxi_error import SaveLocalError, SaveQiniuyunError
from . import haxi_timechange


class ManeouvreMiddle(object):

    @staticmethod
    def get_maneouvre_middle(limit=1, skip=0, desc='-ym_id', fields=[], contions={}):
        fields = fields if fields else database.manoeuvre_middle_fields
        queryset = database_operation.DatabaseOperation(models.ManoeuverMiddle).find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)
        if not queryset:
            return None
        data = []
        for query in queryset:
            query['ym_user'] = models.User.objects.filter(u_id=query['ym_user'])
            query['ym_maneouvre'] = models.Manoeuvre.objects.filter(y_id=query['ym_maneouvre'])
            data.append(query)
        return data

    @staticmethod
    def create_middle_manoeuvre(body, data, text=None):
        # 核实id
        if not (models.ManoeuverMiddle.objects.filter(ym_user__u_id=body['u_id'], ym_manoeuvre__y_id=body['y_id'])):
            return 'bad request'
        #  取出文件
        success_url = list()
        response_url = list()
        try:
            with transaction.atomic():
                for name in ['image', 'video', 'files']:
                    files_url = list()
                    files_data = list()
                    for i in range(1, 11):
                        if not data.get(name+str(i)):
                            break
                        files_data.append(data.get(name+str(i)))
                        # 传出七牛云函数进行储存
                    if files_data:
                        for file_data in files_data:
                            for _ in range(3):  # 保存3次超过三次宣告失败，返回
                                relative_url = haxi_file.File_Operation.save_file(file_data)
                                if relative_url:
                                    break
                                if _ == 2:
                                    raise SaveLocalError('%s保存到本地失败' % file_data.name)
                            absolute_url = os.path.join(settings.MEDIA_ROOT, relative_url)  # 文件相对路径
                            haxi_qiniuyun.Qiniuyun.save_qiniuyun(relative_url, absolute_url)  # 文件绝对路径
                            files_url.append('http://pksdg2zat.bkt.clouddn.com' + '/' + absolute_url)
                            success_url.append(absolute_url)
                            response_url.append('http://pksdg2zat.bkt.clouddn.com' + '/' + relative_url)
                            for t in range(3):
                                retDate, infoDate = haxi_qiniuyun.Qiniuyun.save_qiniuyun(relative_url, absolute_url)
                                # if retDate:
                                #     break
                                # if t == 2:
                                #     os.remove(absolute_url)
                                #     raise SaveQiniuyunError('%s保存到七牛云失败' % file_data.name)
                            os.remove(absolute_url)  # 删除本地文件
                            #  保存url到数据库
                        models.ManoeuverMiddle.objects.filter(ym_manoeuvre__y_id=body['y_id'], ym_user__u_id=body['u_id']).update(**{'ym_{name}_url'.format(name=name): ' '.join(files_url)})
                query = models.ManoeuverMiddle.objects.filter(ym_manoeuvre__y_id=body['y_id'], ym_user__u_id=body['u_id'])
                query.update(ym_finishedtime=haxi_timechange.ChangeTime.change_time_to_date("%Y-%m-%d %H:%M:%S"), ym_finished=True)
                models.Incident.objects.filter(i_symbol=body['y_id'], i_table='manoeuvre').\
                    update(i_symbol=body['y_id'], i_table='manoeuvre', i_endtime=haxi_timechange.ChangeTime.change_time_to_date("%Y-%m-%d %H:%M:%S"))
                if text:
                   query.update(ym_answer=text)
        except SaveLocalError as e:
            for successed in success_url:
                haxi_qiniuyun.Qiniuyun.delete_qiniuyun(successed)
            return e
        except SaveQiniuyunError as e:
            for successed in success_url:
                haxi_qiniuyun.Qiniuyun.delete_qiniuyun(successed)
            return e
        return response_url
        # return fail_files
        # ym_score = models.IntegerField(null=True)
        # ym_timeremaining = models.IntegerField()
        # ym_result = models.CharField(max_length=256, null=True)
        # ym_createtime = models.DateTimeField(auto_now_add=True)
        # ym_changetime = models.DateTimeField(auto_now=True)
        # ym_finished = models.BooleanField(default=False)
        # ym_finishedtime = models.DateTimeField(null=True
