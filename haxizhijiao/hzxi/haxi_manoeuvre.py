# coding: utf-8
import time
from django.db import transaction
from . import database_operation
from . import models
from . import haxi_simple_model_CRUD

class Manoeuvre(object):

    @staticmethod
    def get_manoevure(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Manoeuvre, **body)
        if not data:
            return None
        l = []
        for query in data:
            if query.get('y_createtime'):
                query['y_createtime'] = time.mktime(query['y_createtime'].timetuple())
            if query.get('y_changetime'):
                query['y_changetime'] = time.mktime(query['y_changetime'].timetuple())
            l.append(query)
        return l

    # @staticmethod
    # def get_manoeuvre(limit=1, skip=0, desc='-u_id', fields=[], contions={}):
    #     obj = database_operation.DatabaseOperation(models.Manoeuvre)
    #     fields = fields if fields else database.manoeuvre_fields.copy()
    #     return obj.find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)
    #
    @staticmethod
    def create_manoeuvre(contents):
        i = 0
        data = list()
        with transaction.atomic():
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
                              'ym_user': models.User.objects.get(u_id=u_id),
                              'ym_timeremaining': content['data']['y_endtime']}
                    models.ManoeuverMiddle.objects.create(**fields)
            u_fields = {
                'i_table': 'manoeuvre',
                'i_symbol': y_id
            }
            models.Incident.objects.create(**u_fields)
            i += 1
            print(content)
            from . import database
            queryset = models.Manoeuvre.objects.filter(**content['data']).values(*database.manoeuvre_fields)[0]
            print(queryset)
            if queryset:
                # import json
                # queryset['y_receive'] = (queryset['y_receive'])[1:-1]
                # import pickle


                # print(pickle.loads(bytes(queryset['y_receive'])))
                data.append(queryset)
        return data

    @staticmethod
    def update_manoeuvre(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['data'] # manoeuvre data
            contions = content['contions'] # manoeuvre contions
            if data.get('id_list'):
                receive_id = models.Manoeuvre.objects.get(**contents).y_receive.split(' ')
            if not database_operation.DatabaseOperation(models.Manoeuvre).update(contions=contions, contents=data):
                return 'data %s update error' % i
            # for id in receive_id:
            #     if id in
            #     queryset = models.Manoeuvre.objects.filter(**contions)
            #     for query in queryset:
            #         models.ManoeuverMiddle.objects.filter(mm_manoeuvre__y_id=query['y_id'])
        return None

    @staticmethod
    def delete_manoeuvre(contions):
        i = 0
        try:
            with transaction.atomic():
                for contion in contions:
                    obj = models.Manoeuvre.objects
                    obj.filter(**contion).delete()
                    # models.ManoeuverMiddle.objects.filter(obj.filter(**contion)).delete()
                    i += 1
        except:
            return i


