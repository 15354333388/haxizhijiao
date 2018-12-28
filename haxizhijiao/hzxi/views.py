import simplejson
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
# @api_view(['POST'])
# @permissions.verify_permission # check permissions
def login(request):
    data = {
        'status': 'OK',
        'data': ''
    }
    print('------------------', request.method)
    if request.is_ajax():
        body = json.loads(request.body.decode(encoding='utf-8'))
        u_name = body.get('u_name')
        u_pwd = body.get('u_pwd')
        print('---', u_pwd, u_name)
        query = models.User.objects.filter(u_name=u_name, u_pwd=u_pwd)
        if query:
            data['data'] = 'login successed'
        else:
            data['status'] = 'error'
            data['data'] = 'login failed'
    return JsonResponse(data)


# finsih user register, only receive method of 'post'
# @api_view(['POST', 'GET'])
def register(request):
    data = {
        'status': 'OK',
        'data': ''
    }
    if request.method == 'GET':
        u_pid = str(request.GET.get('u_pid', ''))
        if u_pid:
           query = models.User.objects.get(u_pid=u_pid)
           u_name = query.u_name
           data['u_name'] = u_name
           if query.u_pwd:
               data['status'] = 'error'
               data['data'] = '工号重复'
        else:
            data['status'] = 'error'
        return JsonResponse(data)
    if request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        # a = 'ok' if request.is_ajax() else 'no'
        u_pid = body.get('u_pid')
        u_name = body.get('u_name')
        u_pwd = body.get('u_pwd')
        try:
            query = models.User.objects.get(u_name=u_name, u_pid=u_pid)
            print(request.POST.get('u_pwd', ''))
            query.u_pwd = u_pwd
            query.save()
            data['data'] = 'register successed'
        except Exception as err:
            data['status'] = 'error'
            data['data'] = 'register failed'
        return JsonResponse(data)


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