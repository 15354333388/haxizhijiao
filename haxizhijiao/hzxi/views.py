import simplejson
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from . import permissions
from . import models
# Create your views here.


# index，if not login, must login in index, only and receive method of 'get'
# @api_view(['GET'])
# checked session, if user has login, it will redirect own page
# @permissions.is_login
def index(request):
    return render(request, 'index1.html')


# finish user login, only receive method of 'post'
@api_view(['POST'])
# @permissions.verify_permission # check permissions
def login(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.is_ajax():
        # body = json.loads(request.body.decode(encoding='utf-8'))
        for i in request.data.keys():
            body = json.loads(i)
        u_name = body.get('u_name')
        u_pwd = body.get('u_pwd')
        try:
            query = models.User.objects.get(u_name=u_name, u_pwd=u_pwd)
            data['msg'] = 'login successed'
            return JsonResponse(data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
            data['status'] = 'error'
            data['data'] = 'login failed'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


# finsih user register, only receive method of 'post'
@api_view(['POST', 'GET'])
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
                u_name = query.u_name
                data['u_name'] = u_name
                if query.u_pwd:
                    data['status'] = 'error'
                    data['msg'] = '工号重复'
                if not data['msg']:
                    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(data, status=status.HTTP_200_OK)
            except models.User.MultipleObjectsReturned or models.User.DoesNotExist:
                data['status'] = 'error'
                data['msg'] = 'register failed'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data['status'] = 'error'
            data['msg'] = '没有这个工号'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        # print(request.data)
        # body = json.loads(request.body.decode(encoding='uf-8'))
        dict = request.data
        for i in dict.keys():
            body = json.loads(i)
            print(body, type(body))
            break
        # a = 'ok' if request.is_ajax() else 'no'
        u_pid = body.get('u_pid')
        u_name = body.get('u_name')
        u_pwd = body.get('u_pwd')
        if u_pid and u_name and u_pwd:
            try:
                query = models.User.objects.get(u_name=u_name, u_pid=u_pid)
                query.u_pwd = u_pwd
                query.save()
                data['data'] = 'register successed'
            except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
                data['status'] = 'error'
                data['data'] = 'register failed'
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            data['status'] = 'error'
            data['msg'] = '账号，密码，工会都不能为空'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


# finish user update informations, only receive method of 'update'
# @api_view(['UPDATE'])
def update(request):
    pass


#exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def exam(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass