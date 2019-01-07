# coding: utf-8
from django.db import transaction #开启事务


class DatabaseOperation(object):

    def __init__(self, table):
        self.name = table # appoint table name

    def find(self, fields=[], contions={}, limit=None, skip=None, desc=None):
        print(contions, fields)
        query = self.name.objects.filter(**contions).values(*fields)
        if not query:
            return []
        if desc:
            query = query.order_by(desc)
        if type(limit) == type(skip) == int:
            query = query[skip: skip+limit]
        return query
        # return query.values(*fields).order_by(desc)[start:limit+start] if type(limit) == int else query.values(*fields).order_by(desc)

    def create(self, fields):
        try:
            with transaction.atomic():
                self.name.objects.create(**fields)
                return True
        except Exception:
                print('---none')

    def update(self, contions=None, contents=None):
        try:
            with transaction.atomic():
                self.name.objects.filter(**contions).update(**contents)
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