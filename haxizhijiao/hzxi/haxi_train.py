# coding: utf-8

import time
from django.db import transaction
from . import haxi_simple_model_CRUD
from . import models
from . import database_operation


class Train(object):

    @staticmethod
    def get_train(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Train,**body)
        if not data:
            return None
        l = []
        for query in data:
            if query.get('t_createtime'):
                query['t_createtime'] = time.mktime(query['t_createtime'].timetuple())
            if query.get('u_changetime'):
                query['t_changetime'] = time.mktime(query['t_changetime'].timetuple())
            l.append(query)
        return l

    @staticmethod
    def create_train(contents):
        i = 0
        for content in contents:
            if not (content and type(content) == dict):
                return 'index %s format or content error'
            content['data']['t_endtime'] = int(content['data']['t_endtime'])
            try:
                with transaction.atomic():
                    if not database_operation.DatabaseOperation(models.Train).create(content['data']):
                        return 'create Train table failed, index %s' % i
                    t_id = models.Train.objects.get(**content['data']).t_id #get Train t_id
                    u_pidlist = content.get('pidlist')
                    for u_pid in u_pidlist:
                        query = models.User.objects.get(u_pid=u_pid)
                        u_id = query.u_id
                        fields = {'tm_train': models.Train.objects.get(t_id=t_id),
                                  'tm_user': models.User.objects.get(u_id=u_id),
                                  'tm_timeremaining': content['data']['t_endtime']}
                        if not database_operation.DatabaseOperation(models.TrainMiddle).create(fields):
                            assert 'create TrainMiddle table failed, index %s' % i
            except Exception as err:
                if database_operation.DatabaseOperation(models.Train).delete({'t_id': t_id}):
                    return err
                assert 'delete t_id= %s Train failed' % t_id
            i += 1
        return None

    @staticmethod
    def update_train(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['contens'] # train data
            contions = content['contions'] # train contions
            if not database_operation.DatabaseOperation(models.Train).update(contions=contions, contents=data):
                return 'data %s update error' % i
        return None