# coding: utf-8
import copy
from . import models
from . import database_operation
from . import database
from . import haxi_manoeuvre


class HaxiUser(object):

    @staticmethod
    def get_users(limit=5, skip=0, desc='-u_id', fields=[], contions={}):
        obj = database_operation.DatabaseOperation(models.User)
        if not fields:
            fields = database.user_fields.copy()
            fields.remove('u_pwd')
        return obj.find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def create_user(informations):
        i = 0 # record index
        for information in informations:
            if not (type(information) == dict):
                return i
            obj = database_operation.DatabaseOperation(models.User)
            if not obj.create(information):
                return i
            i += 1

    @staticmethod
    def update_user(informations):
        i = 0
        for information in informations:
            if not (len(information) == 2 and type(information[0]) == type(information[1]) == dict):
                return i
            obj = database_operation.DatabaseOperation(models.User)
            if not obj.update(contions=information[0], content=information[1]):
                return i
            i += 1

    @staticmethod
    def delete_user(contions):
        i = 0
        for contion in contions:
            if not (type(contion) == dict):
                return i
        obj = database_operation.DatabaseOperation(models.User)
        if not obj.delete(contions):
            return i
        i += 1

    # @staticmethod
    # def get_news(fields=[], contions={},limit=1, skip=0, desc='-y_id'):
    #     pass
        # if not (type(contions) == dict and type(fields) == list):
        #     return None
        # queryset = models.User.objects.filter(**contions)
        # if not queryset:
        #     return None
        # ym_fields = fields if fields else database.manoeuvre_middle_fields
        # for query in queryset:
        #     # contions = { filter(lambda field: field, ym_fields)}
        #      mmqueryset = models.ManoeuverMiddle.objects.filter(**contions)：
        #     if mmqueryset:

        # #get manoeuvre
        # contions = {'ym_user': u_id, 'ym_finished':0}
        # fields = ['ym_manoeuvre']
        # print(u_id, contions, fields)
        # query = database_operation.DatabaseOperation(models.ManoeuverMiddle).find(fields, contions=contions)
        # if query:
        #     datadict = {}
        #     maneuverlist = []
        #     print(query)
        #     for foo in query:
        #         result = haxi_manoeuvre.HaxiManoeuvre.get_manoeuvre(contains={'y_id': query['ym_manoeuvre']})
        #         if result:
        #             maneuverlist.append(result)
        #     datadict['maneuverlist'] = maneuverlist
        #     return datadict
