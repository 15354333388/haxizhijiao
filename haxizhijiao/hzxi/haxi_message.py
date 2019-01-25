# coding: utf-8

from . import haxi_simple_model_CRUD
from . import haxi_manoeuvre
from . import models
from . import database


class Message(object):

    @staticmethod
    def get_message(body):
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Message, **body)
        if not data:
            return None
        result = list()
        for d in data:
            query = haxi_manoeuvre.Manoeuvre.get_manoevure({'contions': {'y_id': d['m_symbol']}, 'fields': database.manoeuvre_fields})[0]
            query['is_finish'] = d['m_is_send']
            result.append(query)
        return result