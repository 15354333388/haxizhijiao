# coding: utf-8
from . import  models
from . import database_operation
from . import database

class ManeouvreMiddle(object):

    @staticmethod
    def get_maneouvre_middle(limit=1, skip=0, desc='-ym_id', fields=[], contions={}):
        fields = fields if fields else database.manoeuvre_middle_fields
        queryset = database_operation.DatabaseOperation(models.ManoeuverMiddle).find(fields=fields, contions=contions, limit=limit, skip=skip, desc=desc)
        if not queryset:
            return None
        data = []
        for query in queryset:
            query['ym_user'] = models.User.objects.filter(u_id=['ym_user'])
            query['ym_maneouvre'] = models.Manoeuvre.objects.filter(y_id=query['ym_maneouvre'])
            data.append(query)
        return data