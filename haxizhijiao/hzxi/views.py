#coding: utf-8
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from . import models
from . import permissions
from . import haxi_login
from . import haxi_user
from . import haxi_manoeuvre
# Create your views here.


# index，if not login, must login in index, only and receive method of 'get'
# checked session, if user has login, it will redirect own page
# @permissions.is_login
@api_view(['GET'])
def index(request):
    if request.COOKIES.get('is_login', False):
        try:
            query = models.User.objects.get(u_pid=request.session.get('pid'))
            if query.u_permission == '3':
                return redirect('/hzxi/user/homepage/')
            elif query.u_permission == '2':
                return redirect('/hzxi/admin/homepage/')
        except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
            pass
    return render(request, 'index1.html')


@api_view(['GET'])
@permissions.is_login
def user_home_page(request):
    return render(request, 'personal.html')


@api_view(['GET'])
@permissions.is_login
def admin_home_page(request):
    return render(request, '#')


# finish user login, only receive method of 'post'
@api_view(['POST'])
# @permissions.verify_permission # check permissions
def login(request):
    return haxi_login.HaxiLogin.login(request)


# finsih user register, only receive method of 'post'
@api_view(['POST', 'GET'])
def register(request):
    return haxi_login.HaxiLogin.register(request)

# logout user
@api_view(['POST'])
@permissions.is_login
def logout(request):
    return haxi_login.HaxiLogin.logout(request)


# finish user's information
@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
@permissions.is_login
def user_information(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.is_ajax():
        if request.method == 'GET':
            body = request.GET
            if body:
                u_pid = json.loads(body.get('u_pid'))
                result = haxi_user.HaxiUser.get_user(u_pid=u_pid)
                if result:
                    data['data'] = result[0]
                    return JsonResponse(data, status=status.HTTP_200_OK)
            data['status'] = 'error'
            data['msg'] = 'get user informations failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'POST':
            d = request.data
            body = json.loads(request.body.decode(encoding='utf-8'))
            if haxi_user.HaxiUser.create_user(body):
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            data['status'] = 'error'
            data['msg'] = 'create user failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'UPDATE':
            body = json.loads(request.body.decode(encoding='utf-8'))
            u_pid = body.get('u_pid')
            if u_pid == request.session.get('pid'):
                if haxi_user.HaxiUser.update_user(body, u_pid=u_pid):
                    return JsonResponse(data, status=status.HTTP_201_CREATED)
            data['status'] = 'error'
            data['msg'] = 'update user failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'DELETE':
            body = request.body.decode(encoding='utf-8')
            u_pid = body.get('del_pid')
            if u_pid == request.session.get('pid'):
                return haxi_user.HaxiUser.del_user(u_pid)
            data['status'] = 'error'
            data['msg'] = 'del user failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data['status'] = 'error'
        data['msg'] = 'type error'
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)



#Manoeuvre
def manoeuvre_information(request):
    if request.is_ajax():
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            d = request.data
            body = json.loads(request.body.decode(encoding='utf-8'))
            if  body['u_pid'] == request.session['pid']:
                return haxi_manoeuvre.HaxiManoeuvre.create_manoeuvre(body)



#exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def exam(request):
    if request.method == 'GET':
        models.User.objects.create(u_name='123')
        return HttpResponse('exam')
    if request.method == 'POST':
        pass


