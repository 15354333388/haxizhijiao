# coding: utf-8
from . import  models
from . import database_operation
from . import database
from . import save_qiniuyun

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
        #  取出文件
        for name in ['image', 'video', 'file']:
            file_data, fail_files = [], []
            for i in range(1, 11):
                if not data.get(name+str(i)):
                    break
                file_data.append(data.get(name+str(i)))
                # 传出七牛云函数进行储存
            if file_data:
                print(file_data)
                url, data = save_qiniuyun.save_niuyun(file_data)
                print(url, data)
                fail_files += [i.name for i in data]
                    # if not url:
                    #     assert "save %s qiniuyun failed" % name
                    #     # 删除以保存的部分
                    #     models.ManoeuverMiddle.objects.filter(**body).update(ym_image_url=None, ym_video_url=None, ym_files_url=None)
                    # 保存url到数据库
                models.ManoeuverMiddle.objects.filter(**body).update(**{'ym_(0)_url'.format(name): ' '.join(url)})
                if text:
                    models.Manoeuvre.objects.filter(**body).update(ym_answer=text)
        return fail_files



