# coding: utf-8
from . import models
from . import database_operation
from . import database


class TrainMiddle(object):

    @staticmethod
    def get_train_middle(limit=1, skip=0, desc='-tm_id', fields=[], contions={}):
        fields = fields if fields else database.train_middle_fields
        queryset = database_operation.DatabaseOperation.find(fields=fields, contions=contions, limit=limit, skip=skip,
                                                             desc=desc)
        if not queryset:
            return None
        data = []
        for query in queryset:
            query['tm_user'] = models.User.objects.filter(u_id=['ym_user'])
            query['tm_train'] = models.Manoeuvre.objects.filter(y_id=query['tm_train'])
            data.append(query)
        return data