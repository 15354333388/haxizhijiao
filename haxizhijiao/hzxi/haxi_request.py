# coding: utf-8

import json
from . import database
from . import models

fieldsList = {
    models.User: database.user_fields,
    models.Manoeuvre: database.manoeuvre_fields,
    models.ManoeuverMiddle: database.manoeuvre_middle_fields,
    models.Bank: database.bank_fields,
    models.Examine: database.examine_fields,
    models.ExamineMiddle: database.examine_middle_fields,
    models.Train: database.train_fields,
    models.TrainMiddle: database.train_middle_fields,
    models.Work: database.work_fields,
    models.WorkMiddle: database.work_middle_fields,
    models.Incident: database.incident_fields,
}

class HaxiRequest(object):
    @staticmethod
    def get_request_contions(request):
        body = request.GET
        contions = json.loads(body.get('contions')) if body.get('contions') else {} # inquire contions
        fields = json.loads(body.get('fields')).split(' ') if body.get('fields') else [] # inquire fields
        limit = int(json.loads(body.get('limit'))) if body.get('limit') else None # inquire umber
        skip = int(json.loads(body.get('skip'))) if body.get('skip') else None # inquire start position
        return {'fields': fields, 'contions': contions, 'limit': limit, 'skip': skip}

# data: { contions:{}, fields: [], limit: int, skip: int, desc: str }