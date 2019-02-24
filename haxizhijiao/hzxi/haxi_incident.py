# coding: utf-8

import time
from . import models
from . import haxi_simple_model_CRUD
from . import database
from . import haxi_manoeuvre
from . import haxi_train
from . import haxi_work
from . import haxi_examine_bank


class Incident(object):
    @staticmethod
    def get_incident(body):
        def deal_manoeuvre(id):
            return haxi_manoeuvre.Manoeuvre.get_manoevure({'fields': database.manoeuvre_fields, 'contions': {'y_id': id}})
        def deal_work(id):
            return haxi_work.Work.get_work({'fields': database.work_fields, 'contions': {'w_id': id}})
        def deal_examine(id):
            return haxi_examine_bank.Examine.get_examine({'fields': database.examine_fields, 'contions': {'e_id': id}})
        def deal_train(id):
            return haxi_train.Train.get_train({'fields': database.train_fields, 'contions': {'t_id': id}})
        func = {
            'manoeuvre': deal_manoeuvre,
            'train': deal_train,
            'work': deal_work,
            'examine': deal_examine,
        }
        data = haxi_simple_model_CRUD.HaxiSimpleCrud.get(models.Incident, **body)
        if not data:
            return None
        l = []
        for query in data:
            if query.get('i_createtime'):
                print(time.mktime(query['i_createtime'].timetuple()))
                query['i_createtime'] = time.mktime(query['i_createtime'].timetuple())
            if query.get('i_endtime'):
                query['i_endtime'] = time.mktime(query['i_endtime'].timetuple())
            query['content'] = [x for x in func[query['i_table']](query['i_symbol'])]
            l.append(query)
        return l

    # @staticmethod
    # def create(informations):
    #     return haxi_simple_model_CRUD.HaxiSimpleCrud.create(models.Incident, informations)
    #
    # @staticmethod
    # def update(informations):
    #     return haxi_simple_model_CRUD.HaxiSimpleCrud.update(models.Incident, informations)
    # @staticmethod
    # def delete(contions):
    #     return haxi_simple_model_CRUD.HaxiSimpleCrud.delete(models.Incident, contions)