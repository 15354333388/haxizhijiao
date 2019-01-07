# coding: utf-8
# time: 2018-12-27 14:46

from . import models
#exam class has all functions about exam
class Exam(object):
    @staticmethod
    def add_exam():
        pass

    @staticmethod
    def get_examInformations(jobNumber=None):
        if jobNumber: # get single unfinished exam
            queryset = models.HaxiExamHistory.objects.filter(staffId_jobNumber= jobNumber, examStatus=0)
            l = []
            for query in queryset:
                d = {}
                q = models.HaxiExam.get(id=query['examId'])
                d['id'] = q['id']
                d['exam_name'] = q['exam_name']
                d['exam_intro'] = q['exam_intro']


    @staticmethod
    def get_examHistory():
        pass