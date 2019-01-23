# coding: utf-8
from . import database_operation


class HaxiSimpleCrud(object):

    @staticmethod
    def get(table, limit=None, skip=None, desc=None, fields=[], contions={}):
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
            contions = information.get('contions')
            if contions.get('u_id'):
                contions['u_id'] = int(contions['u_id'])
            contents = information.get('content')
            if not database_operation.DatabaseOperation(table).update(contions=contions, contents=contents):
                return i
            i += 1

    @staticmethod
    def delete(table, contions):
        i = 0
        for contion in contions:
            if not (type(contion) == dict and contion):
                return i
        if not database_operation.DatabaseOperation(table).delete(contion):
            return i
        i += 1
