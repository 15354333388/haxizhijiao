# coding: utf-8
import time
import json
from django.http import JsonResponse
from rest_framework import status
from . import models


class HaxiLogin(object):

    @staticmethod
    def login(request):
        data = {
            'status': 'OK',
            'msg': '',
            'data': ''
        }
        if request.is_ajax():
            body = json.loads(request.body.decode(encoding='utf-8'))
            u_pid = body.get('u_pid')
            u_pwd = body.get('u_pwd')
            try:
                query = models.User.objects.get(u_pid=u_pid, u_pwd=u_pwd)
                data['msg'] = 'login successed'
                response = JsonResponse(data, status=status.HTTP_200_OK)
                response.set_cookie('is_login', 'True')
                request.session['pid'] = query.u_pid
                return response
            except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
                data['status'] = 'error'
                data['data'] = 'login failed'
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def register(request):
        data = {
            'status': 'OK',
            'msg': '',
            'data': ''
        }
        if request.method == 'GET':
            u_pid = str(request.GET.get('u_pid', ''))
            if u_pid:
                try:
                    query = models.User.objects.get(u_pid=u_pid)
                    query.save()
                    u_name = query.u_name
                    data['u_name'] = u_name
                    if query.u_pwd:
                        data['status'] = 'error'
                        data['msg'] = '工号重复'
                    if data['msg']:
                        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                    return JsonResponse(data, status=status.HTTP_200_OK)
                except models.User.MultipleObjectsReturned and models.User.DoesNotExist:
                    data['status'] = 'error'
                    data['msg'] = 'register failed'
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['status'] = 'error'
                data['msg'] = '没有这个工号'
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            body = json.loads(request.body.decode(encoding='utf-8'))
            # a = 'ok' if request.is_ajax() else 'no'
            u_pid = body.get('u_pid')
            u_name = body.get('u_name')
            u_pwd = body.get('u_pwd')
            if u_pid and u_name and u_pwd:
                if not models.User.objects.filter(u_pwd=u_pwd):
                    try:
                        query = models.User.objects.get(u_name=u_name, u_pid=u_pid)
                        query.u_pwd = u_pwd
                        query.save()
                        data['data'] = 'register successed'
                        response = JsonResponse(data, status=status.HTTP_201_CREATED)
                        response.set_cookie('is_login', 'True')
                        request.session['pid'] = query.u_pid
                        return response
                    except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
                        data['status'] = 'error'
                        data['data'] = 'register failed'
                        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                data['status'] = 'error'
                data['msg'] = '密码不可用'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data['status'] = 'error'
                data['msg'] = '账号，密码，工号都不能为空'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def logout(request):
        data = {
            'status': 'OK',
            'msg': '',
            'data': ''
        }
        body = json.loads(request.body.decode(encoding='utf-8'))
        u_pid = body.get('u_pid')
        query = models.User.objects.filter(u_pid=u_pid)
        if len(query) == 1:
            del request.session['name']
            del request.session['pid']
            response = JsonResponse(data, status=status.HTTP_200_OK)
            response.set_cookie('is_login', False)
            return response
        else:
            data['status'] = 'error'
            data['msg'] = 'not found informations, logout failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


