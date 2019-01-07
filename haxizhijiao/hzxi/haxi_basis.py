# coding: utf-8

from django.db import transaction
from . import models
from . import database_operation
from . import database


class HaxiBasic(object):

    @staticmethod
    def get_examine(limit=1, skip=0, desc='-e_id', fields=[], contions={}):
        obj = database_operation.DatabaseOperation(models.Examine)
        fields = fields if fields else database.examine_fields.copy()
        return obj.find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def create_examine(contents):
        i = 0
        for content in contents:
            if not (content and type(content) == dict):
                return 'index %s format or content error'
            content['data']['e_endtime'] = int(content['data']['e_endtime'])
            try:
                with transaction.atomic():
                    if not database_operation.DatabaseOperation(models.Examine).create(content['data']):
                        return 'create Train table failed, index %s' % i
                    e_id = models.Examine.objects.get(**content['data']).e_id  # get Train t_id
                    u_pidlist = content.get('pidlist')
                    for u_pid in u_pidlist:
                        query = models.User.objects.get(u_pid=u_pid)
                        u_id = query.u_id
                        fields = {'em_examine': models.Examine.objects.get(e_id=e_id),
                                  'em_user': models.User.objects.get(u_id=u_id),
                                  'em_timeremaining': content['data']['e_endtime']}
                        if not models.ManoeuverMiddle.objects.create(**fields):
                            assert 'create ExamineMiddle table failed, index %s' % i
            except Exception as err:
                if database_operation.DatabaseOperation(models.Examine).delete({'t_id': e_id}):
                    return err
                assert 'delete t_id= %s Examine failed' % e_id
            i += 1
        return None