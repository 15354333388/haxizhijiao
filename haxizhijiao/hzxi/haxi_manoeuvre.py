# coding: utf-8
from django.db import transaction
from . import models
from . import database
from . import database_operation

class HaxiManoeuvre(object):

    @staticmethod
    def get_manoeuvre(limit=1, skip=0, desc='-u_id', fields=[], contions={}):
        print(limit, skip, desc, fields, contions)
        obj = database_operation.DatabaseOperation(models.Manoeuvre)
        fields = fields if fields else database.manoeuvre_fields.copy()
        return obj.find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def create_manoeuvre(contents):
        # d = {key:content.get(key) for key in filter(lambda field:content.get(field), fields)}
        # for field in fields:
        #     if content.get(field, None):
        #         d[field] =content.get(field)
        i = 0
        for content in contents:
            if not (content and type(content) == dict):
                return 'index %s format or content error'
            try:
                with transaction.atomic():
                    if not database_operation.DatabaseOperation(models.Manoeuvre).create(**content['data']):
                        assert 'create Manoeuver table failed, index %s' % i
                    y_id = models.Manoeuvre.objects.get(**content['data']).y_id #get manoeuvre y_id
                    u_pidlist = content.get('pidlist')
                    for u_pid in u_pidlist:
                        query = database_operation.DatabaseOperation(models.User).find({'u_pid': u_pid})
                        if query:
                            u_id = query['u_id']
                            fields = {'ym_manoeuvre': y_id, 'ym_user': u_id, 'ym_timeremaining': content.get('y_endtime')}
                            if not models.ManoeuverMiddle.objects.create(**fields):
                                assert 'create ManoeuverMiddle table failed, index %s' % i
                        else:
                            assert 'user not find'
            except Exception as err:
                database_operation.DatabaseOperation(models.Manoeuvre).delete({'y_id': y_id})
                return err
            i += 1
        return None

