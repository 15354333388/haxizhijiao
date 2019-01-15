# coding: utf-8
import json
from django.http import JsonResponse
from rest_framework import status
from . import models
from . import database


class HaxiLogin(object):

    @staticmethod
    def login(request):
        data = database.data
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
            data['data'] = 'login failed, PID or password error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def register(request):
        data = database.data
        if request.method == 'GET':
            u_pid = str(request.GET.get('u_pid'))
            if not u_pid:
                data['status'] = 'error'
                data['msg'] = 'no pid'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            try:
                query = models.User.objects.get(u_pid=u_pid)
                query.save()
                u_name = query.u_name
                data['u_name'] = u_name
                if query.u_pwd:
                    data['status'] = 'error'
                    data['msg'] = 'pid number is not only one'
                if data['msg']:
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(data, status=status.HTTP_200_OK)
            except models.User.MultipleObjectsReturned and models.User.DoesNotExist:
                data['status'] = 'error'
                data['msg'] = 'not found PID'
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':
            body = json.loads(request.body.decode(encoding='utf-8'))
            u_pid = body.get('u_pid')
            u_name = body.get('u_name')
            u_pwd = body.get('u_pwd')
            if not (u_pid and u_name and u_pwd):
                data['status'] = 'error'
                data['msg'] = 'account,password,PID error'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
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
                    data['data'] = 'PID or account is not exist'
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            data['status'] = 'error'
            data['msg'] = 'password is not invalid'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def logout(request):
        data = database.data
        body = json.loads(request.body.decode(encoding='utf-8'))
        u_pid = body.get('u_pid')
        query = models.User.objects.filter(u_pid=u_pid)
        if not (len(query) == 1):
            data['status'] = 'error'
            data['msg'] = 'not found PID, logout failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        del request.session['name']
        del request.session['pid']
        response = JsonResponse(data, status=status.HTTP_200_OK)
        response.set_cookie('is_login', False)
        return response


