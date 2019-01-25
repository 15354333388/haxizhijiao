# coding: utf-8
import json
import copy
from django.http import JsonResponse
from rest_framework import status
from . import models
from . import database
from . import haxi_timechange


class HaxiLogin(object):

    @staticmethod
    def login(request):
        data = copy.deepcopy(database.data)
        body = json.loads(request.body.decode(encoding='utf-8'))
        u_pid = body.get('u_pid')
        u_pwd = body.get('u_pwd')
        try:
            query = models.User.objects.get(u_pid=u_pid, u_pwd=u_pwd)
            data['msg'] = 'login successed'
            data['name'] = query.u_name
            data['id'] = query.u_id
            response = JsonResponse(data, status=status.HTTP_200_OK)
            response.set_cookie('is_login', 'True')
            request.session['pid'] = query.u_pid
            response['Access-Control-Allow-Origin'] = "*"
            # save LoginUser table
            models.LoginUser.objects.create(l_u_id=query.u_id)
        except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
            data['status'] = 'error'
            data['data'] = 'login failed, PID or password error'
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            response['Access-Control-Allow-Origin'] = "*"
        return response

    @staticmethod
    def register(request):
        data = copy.deepcopy(database.data)
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
    def logout(request, clients):
        data = copy.deepcopy(database.data)
        body = json.loads(request.body.decode(encoding='utf-8'))
        u_id = int(body['u_id']) if body.get('u_id') else None
        if not u_id:
            data['status'] = 'error'
            data['msg'] = 'no ID, logout failed'
            print(data)
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            res['Access-Control-Allow-Origin'] = "*"
            return res
        if not clients.get(u_id):
            data['status'] = 'error'
            data['msg'] = 'account has noe logined, logout failed'
            print(data)
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            res['Access-Control-Allow-Origin'] = "*"
            return res
        del clients[u_id]
        query = models.User.objects.filter(u_id=u_id)
        if not (len(query) == 1):
            data['status'] = 'error'
            data['msg'] = 'nou found database, logout failed'
            print(data)
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            res['Access-Control-Allow-Origin'] = "*"
            return res
        # del request.session['name']
        # del request.session['pid']
        changetime = haxi_timechange.ChangeTime.change_time_to_date('%Y-%m-%d %H:%M:%S')
        models.LoginUser.objects.filter(l_u_id=u_id, l_islogin=True).update(l_islogin=False, l_changetime=changetime)
        response = JsonResponse(data, status=status.HTTP_200_OK)
        response.set_cookie('is_login', False)
        response['Access-Control-Allow-Origin'] = "*"
        return response


