# coding: utf-8
from django.db import transaction
from . import models
from . import database
from . import database_operation

class HaxiManoeuvre(object):

    @staticmethod
    def get_manoeuvre(limit=1, skip=0, desc='-u_id', fields=[], contions={}):
        obj = database_operation.DatabaseOperation(models.Manoeuvre)
        fields = fields if fields else database.manoeuvre_fields.copy()
        return obj.find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)

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
                assert 'delete y_id= %s Manoeuvre failed' % y_id
            i += 1
        return None

    @staticmethod
    def update_manoeuvre(contents):
        for content in contents:
            i = 0
            if not (content and type(content) == dict):
                return 'content %s type error' % i
            data = content['data'] # manouvre data
            contions = {
                'ym_user__u_pid': content['u_pid'] # user pid
            }
            if not database_operation.DatabaseOperation.update(contions=contions, contents=data):
                return 'data %s update error' % i
        return None


