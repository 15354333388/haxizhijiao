# coding: utf-8
from . import models
from . import database_operation
from . import database


class HaxiUser(object):
    @staticmethod
    def get_user(limit=1, skip=0, desc='-u_id', **kwargs):
        obj = database_operation.DatabaseOperation(models.User)
        fields = database.user_fields
        return obj.findOne(fields, contions=kwargs, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def get_users(limit=1, skip=0, desc='-u_id', **kwargs):
        obj = database_operation.DatabaseOperation(models.User)
        fields = database.user_fields
        return obj.find(fields, contions=kwargs, limit=limit, skip=skip, desc=desc)

    @staticmethod
    def create_user(body):
        d = {}
        for field in database.user_fields:
            if body.get(field, None):
                d[field] = body.get(field)
        obj = database_operation.DatabaseOperation(models.User)
        return obj.create(d)

    @staticmethod
    def update_user(body, **kwargs):
        update_dict = {}
        for field in database.user_fields:
            if body.get(field):
                update_dict[field] = body.get(field)
        print(update_dict, '--------------', kwargs)
        obj = database_operation.DatabaseOperation(models.User)
        return obj.update(contions=kwargs, fields=update_dict)

    @staticmethod
    def delete_user(body):
        obj = database_operation.DatabaseOperation(models.User)
        return obj.delete(body)