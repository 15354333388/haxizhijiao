# coding: utf-8
from django.db import transaction #开启事务


class DatabaseOperation(object):

    def __init__(self, table):
        self.name = table # appoint table name

    def findOne(self, fields, contions=None, limit=1, skip=0, desc='-u_id'): #
        query = self.name.objects.filter(**contions)
        if len(query) == 1:
            print('------------------', query)
            return query.values(*fields).order_by(desc)[skip:limit+skip]

    def find(self, fields, contions=None, limit=1, skip=0, desc='-u_id'):
        query = self.name.objects.filter(**contions)
        if query:
            return query.values(*fields).order_by(desc)[skip:limit+skip]

    def create(self, fields):
        try:
            with transaction.atomic():
                self.name.objects.create(**fields)
                return True
        except Exception:
            return None

    def update(self, contions=None, fields=None):
        try:
            with transaction.atomic():
                self.name.objects.filter(**contions).update(**fields)
                return True
        except Exception:
            return None

    def delete(self, fields):
        try:
            with transaction.atomic():
                self.name.objects.filter(**fields).delete()
                return True
        except Exception:
            return None