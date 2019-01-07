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
        for content in contents:
            if not (content and type(content) == dict):
                return 'index %s format or content error'
            content['data']['y_endtime'] = int(content['data']['y_endtime'])
            try:
                with transaction.atomic():
                    if not database_operation.DatabaseOperation(models.Manoeuvre).create(content['data']):
                        return 'create Manoeuver table failed, index %s' % i
                    y_id = models.Manoeuvre.objects.get(**content['data']).y_id #get manoeuvre y_id
                    u_pidlist = content.get('pidlist')
                    for u_pid in u_pidlist:
                        query = models.User.objects.get(u_pid=u_pid)
                        u_id = query.u_id
                        fields = {'ym_manoeuvre': models.Manoeuvre.objects.get(y_id=y_id),
                                  'ym_user': models.User.objects.get(u_id=u_id),
                                  'ym_timeremaining': content['data']['y_endtime']}
                        if not models.ManoeuverMiddle.objects.create(**fields):
                            assert 'create ManoeuverMiddle table failed, index %s' % i
            except Exception as err:
                if database_operation.DatabaseOperation(models.Manoeuvre).delete({'y_id': y_id}):
                    return err
                assert 'delete y_id= %s Manoeuvre failed, please delete with hand ' % y_id
            u_fields = {
                'ui_table': 'manoeuvre',
                'ui_symbol': y_id
            }
            if not database_operation.DatabaseOperation(models.UnfinshedIncident).create(u_fields):
                assert 'create unfinished failed index %s' % i
            i += 1
        return None

    @staticmethod
    def update_manoeuvre(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['contens'] # manoeuvre data
            contions = content['contions'] # manoeuvre contions
            if not database_operation.DatabaseOperation(models.Manoeuvre).update(contions=contions, contents=data):
                return 'data %s update error' % i
            # if data.get('u_pidlist'):
            #     queryset = models.Manoeuvre.objects.filter(**contions)
            #     for query in queryset:
            #         models.ManoeuverMiddle.objects.filter(mm_manoeuvre__y_id=query['y_id'])
        return None


