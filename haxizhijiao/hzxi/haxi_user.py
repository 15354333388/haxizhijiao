# coding: utf-8

import time
from . import models
from . import haxi_simple_model_CRUD
from . import haxi_timechange


class User(object):
    @staticmethod
    def get(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.User,**body)
        if not data:
            return None
        l = list()
        for query in data:
            if query.get('u_createtime'):
                # time.mktime(date.timetuple())
                query['u_createtime'] = time.mktime(query['u_createtime'].timetuple())
            if query.get('u_changetime'):
                query['u_changetime'] = time.mktime(query['u_changetime'].timetuple())
            if query.get('u_sex'):
                query['u_sex'] = '男' if query['u_sex'] == '1' else '女'
            # print(query)
            l.append(query)
        return l

    @staticmethod
    def create(informations):
        return haxi_simple_model_CRUD.HaxiSimpleCrud.create(models.User, informations)

    @staticmethod
    def update(informations):
        return haxi_simple_model_CRUD.HaxiSimpleCrud.update(models.User, informations)

    @staticmethod
    def delete(contions):
        return haxi_simple_model_CRUD.HaxiSimpleCrud.delete(models.User, contions)