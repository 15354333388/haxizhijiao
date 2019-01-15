# coding: utf-8
from . import database_operation


class HaxiSimpleCrud(object):

    @staticmethod
    def get(table, limit=None, skip=None, desc=None, fields=[], contions={}):
        print('+++++++++++++++++++++++', table, limit, skip, desc, fields, contions)
        return database_operation.DatabaseOperation(table).find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def create(table, informations):
        i = 0  # record index
        for information in informations:
            if not (type(information) == dict):
                return i
            obj = database_operation.DatabaseOperation(table)
            if not obj.create(information):
                return i
            i += 1
        return None

    @staticmethod
    def update(table, informations):
        i = 0
        for information in informations:
            if not (type(information) == dict and information):
                return i
            if not database_operation.DatabaseOperation(table).update(contions=information[0], content=information[1]):
                return i
            i += 1

    @staticmethod
    def delete(table, contions):
        i = 0
        for contion in contions:
            if not (type(contion) == dict):
                return i
        if not database_operation.DatabaseOperation(table).delete(contions):
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
