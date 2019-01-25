# coding: utf-8
import time
from django.db import transaction
from . import database_operation
from . import models
from . import haxi_simple_model_CRUD
from . import haxi_timechange
from . import database


class Manoeuvre(object):

    @staticmethod
    def get_manoevure(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Manoeuvre, **body)
        if not data:
            return None
        l = list()
        for query in data:
            if query.get('y_createtime'):
                query['y_createtime'] = haxi_timechange.ChangeTime.change_date_to_time(query['y_createtime'])
            if query.get('y_changetime'):
                query['y_changetime'] = haxi_timechange.ChangeTime.change_date_to_time(query['y_changetime'])
            l.append(query)
        return l

    @staticmethod
    def create_manoeuvre(contents):
        i = 0
        data = list()
        with transaction.atomic():  # 开启事务，保障内容的一致性
            for content in contents:
                if not (content and type(content) == dict):
                    return 'index %s format or content error' % i
                content['data']['y_endtime'] = int(content['data']['y_endtime'])
                content['data']['y_receive'] = ' '.join(content['data']['y_receive'])
                models.Manoeuvre.objects.create(**content['data'])
                y_id = models.Manoeuvre.objects.get(**content['data']).y_id #get Examine e_id
                id_list = content.get('id_list')
                for u_id in id_list:
                    fields = {'ym_manoeuvre': models.Manoeuvre.objects.get(y_id=y_id),
                              'ym_user': models.User.objects.get(u_id=int(u_id)),
                              'ym_timeremaining': content['data']['y_endtime']}
                    models.ManoeuverMiddle.objects.create(**fields)
            u_fields = {
                'i_table': 'manoeuvre',
                'i_symbol': y_id
            }
            models.Incident.objects.create(**u_fields)
            i += 1
            queryset = models.Manoeuvre.objects.filter(**content['data']).values('y_id', 'y_receive')[0]
            print(queryset)
            if queryset:
                queryset['type'] = 'manoeuvre'
                data.append(queryset)
        return data

    @staticmethod
    def update_manoeuvre(contents):
        for content in contents:
            i = 0
            with transaction.atomic():
                if not (content and type(content) == dict):
                    return i
                data = content['data'] # manoeuvre data
                if data.get('y_endtime'):
                    data['y_endtime'] = int(data['y_endtime'])
                    models.ManoeuverMiddle.objects.filter(ym_manoeuvre__y_id=models.Manoeuvre.objects.get(**contions).y_id).\
                                                                            update({'ym_timeremaining': data['y_endtime']})
                contions = content['contions'] # manoeuvre contions
                models.Manoeuvre.objects.filter(**contions).filter(**data) #
        return None

    @staticmethod
    def delete_manoeuvre(contions):
        i = 0
        try:
            with transaction.atomic():
                for contion in contions:
                    queryset = models.Manoeuvre.objects.filter(**contion)  # 删除manoeuvre
                    if queryset:
                        l = list()
                        for query in queryset:
                            l.append(query['y_id'])
                        queryset.delete()
                    for id in l:
                        models.Incident.objects.filter(i_table='manoeuvre', i_symbol=id).delete()
                    # models.ManoeuverMiddle.objects.filter(obj.filter(**contion)).delete()
                    i += 1
        except:
            return i


