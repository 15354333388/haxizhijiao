# coning: utf-8
import time
from django.db import transaction
from . import database
from . import database_operation
from . import models
from . import haxi_simple_model_CRUD


class Examine(object):
    @staticmethod
    def get_bank(limit=None, skip=None, desc='-b_id', fields=[], contions={}):
        fields = fields if fields else database.bank_fields.copy()
        return database_operation.DatabaseOperation(models.Bank).find(limit=limit, skip=skip, desc=desc, fields=fields, contions=contions)

    @staticmethod
    def get_examine(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Examine,**body)
        if not data:
            return None
        l = []
        for query in data:
            if query.get('e_createtime'):
                query['e_createtime'] = time.mktime(query['e_createtime'].timetuple())
            if query.get('e_changetime'):
                query['e_changetime'] = time.mktime(query['e_changetime'].timetuple())
            l.append(query)
        return l

    @staticmethod
    def create_examine(contents):
        i = 0
        for content in contents:
            if not (content and type(content) == dict):
                return 'index %s format or content error'
            content['data']['e_endtime'] = int(content['data']['e_endtime'])
            try:
                with transaction.atomic():
                    if not database_operation.DatabaseOperation(models.Manoeuvre).create(content['data']):
                        return 'create Examine table failed, index %s' % i
                    e_id = models.Examine.objects.get(**content['data']).e_id #get Examine e_id
                    u_pidlist = content.get('pidlist')
                    for u_pid in u_pidlist:
                        query = models.User.objects.get(u_pid=u_pid)
                        u_id = query.u_id
                        fields = {'em_examine': models.Examine.objects.get(e_id=e_id),
                                  'em_user': models.User.objects.get(u_id=u_id),
                                  'em_timeremaining': content['data']['e_endtime']}
                        if not models.ExamineMiddle.objects.create(**fields):
                            assert 'create ExamineMiddle table failed, index %s' % i
            except Exception as err:
                if database_operation.DatabaseOperation(models.Examine).delete({'y_id': e_id}):
                    return err
                assert 'delete e_id= %s Manoeuvre failed, please delete with hand ' % e_id
            u_fields = {
                'ui_table': 'examine',
                'ui_symbol':e_id
            }
            if not database_operation.DatabaseOperation(models.UnfinshedIncident).create(u_fields):
                assert 'create unfinished failed index %s' % i
            i += 1
        return None

    @staticmethod
    def update_examine(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['contens'] # manoeuvre data
            contions = content['contions'] # manoeuvre contions
            if not database_operation.DatabaseOperation(models.Examine).update(contions=contions, contents=data):
                return 'data %s update error' % i
            # if data.get('u_pidlist'):
            #     queryset = models.Manoeuvre.objects.filter(**contions)
            #     for query in queryset:
            #         models.ManoeuverMiddle.objects.filter(mm_manoeuvre__y_id=query['y_id'])
        return None