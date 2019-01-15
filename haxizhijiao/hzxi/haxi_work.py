# coding: utf-8
import time

from django.db import transaction
from . import haxi_simple_model_CRUD
from . import models
from . import database_operation

class Work(object):

    @staticmethod
    def get_work(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Work, **body)
        if not data:
            return None
        l = []
        for query in data:
            if query.get('w_createtime'):
                query['w_createtime'] = time.mktime(query['w_createtime'].timetuple())
            if query.get('w_changetime'):
                query['w_changetime'] = time.mktime(query['w_changetime'].timetuple())
            l.append(query)
        return l

    @staticmethod
    def create_work(contents):
        i = 0
        with transaction.atomic():
            for content in contents:
                if not (content and type(content) == dict):
                    return 'index %s format or content error'
                content['data']['w_endtime'] = int(content['data']['w_endtime'])
                models.Work.objects.create(**content['data'])
                w_id = models.Work.objects.get(**content['data']).w_id #get Examine w_id
                u_pidlist = content.get('pidlist')
                for u_pid in u_pidlist:
                    query = models.User.objects.get(u_pid=u_pid)
                    u_id = query.u_id
                    fields = {'em_examine': models.Work.objects.get(w_id=w_id),
                                'em_user': models.User.objects.get(u_id=u_id),
                                'em_timeremaining': content['data']['e_endtime']}
                    models.WorkMiddle.objects.create(**fields)
            u_fields = {
                'ui_table': 'work',
                'ui_symbol':w_id
            }
            models.Incident.objects.create(**u_fields)
            i += 1
        return None

    @staticmethod
    def update_work(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['contens'] # manoeuvre data
            contions = content['contions'] # manoeuvre contions
            if not database_operation.DatabaseOperation(models.Work).update(contions=contions, contents=data):
                return 'data %s update error' % i
        return None