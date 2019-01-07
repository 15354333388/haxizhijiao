#coding: utf-8
import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from . import models
from . import permissions
from . import haxi_login
from . import haxi_user
from . import haxi_manoeuvre
from . import haxi_request
from . import haxi_train
from . import haxi_basis
from . import haxi_maneouvre_middle
from . import haxi_train_middle
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
# @permissions.is_login
def user_home_page(request):
    return render(request, 'personal.html')


@api_view(['GET'])
# @permissions.is_login
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
# @permissions.is_login
def logout(request):
    return haxi_login.HaxiLogin.logout(request)


# finish user's information
@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
# @permissions.is_login
@permissions.is_ajax
# @permissions.is_same
def user_information(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': []
    }
    # if request.is_ajax():
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-u_id'
        result = haxi_user.HaxiUser.get_users(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        informations = body.get('userInformations')
        if informations and type(informations) == list:
            result = haxi_user.HaxiUser.create_user(informations)
            if result:
                data['status'] = 'error'
                data['msg'] = 'part users have created, but index is %s error' % result
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(data, status==status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = 'new user is lack of contions, or bad request'
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'UPDATE':
        body = json.loads(request.body.decode(encoding='utf-8'))
        updateDate = body.get('updateDate', [])
        if not (type(updateDate) == list and updateDate):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_user.HaxiUser.update_user(updateDate)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part update have created, but index is %s error' % result
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = 'informations is error'
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        body = request.body.decode(encoding='utf-8')
        contions = body.get('contions', {})
        if not (contions and type(contions) == dict):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_user.HaxiUser.delete_user(contions)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part user have delete, but index is %s error' % result
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data, status=status.HTTP_200_OK)



#Manoeuvre
@api_view(['GET', 'POST', 'UPDATE'])
# @permissions.is_login
@permissions.is_ajax
def manoeuvre(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    # if request.is_ajax():
    print(request.method)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-y_id'
        result = haxi_manoeuvre.HaxiManoeuvre.get_manoeuvre(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get manoeuver failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        for query in result:
            query['y_createtime'] = time.mktime(query['y_createtime'].timetuple())
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create manoeuver failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_manoeuvre.HaxiManoeuvre.create_manoeuvre(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'UPDATE': # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create manoeuver failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_manoeuvre.HaxiManoeuvre.update_manoeuvre(contents)
        if result:
            data['status'] = 'error'
            data['msg'] = result
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data, status=status.HTTP_200_OK)


# manoeuvremiddle view
@api_view(['GET'])
def manoeuver_middle(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-ym_id'
        result = haxi_maneouvre_middle.ManeouvreMiddle.get_maneouvre_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)


# # user request all news
# @api_view(['GET', 'POST'])
# # @permissions.is_login
# # @permissions.is_ajax
# # @permissions.is_same
# def user_news(request):
#     data = {
#         'status': 'OK',
#         'msg': '',
#         'data': ''
#     }
#     print('method', request.method)
#     if request.method == 'GET':
#         body = request.GET
#         contions = json.loads(body.get('contions')) if body.get('contions') else {}  # inquire contions
#         # fields = json.loads(body.get('fields')).split(' ') if body.get('fields') else None  # inquire fields
#         limit = int(json.loads(body.get('limit'))) if body.get('limit') else 1  # inquire umber
#         skip = int(json.loads(body.get('skip'))) if body.get('skip') else 0  # inquire start position
#         desc = json.loads(body.get('desc')) if body.get('desc') else '-u_id'  # desc method
#         fields = ['u_id']
#         u_result = haxi_user.HaxiUser.get_users(contions=contions, fields=fields, limit=limit, skip=skip, desc=desc)
#
#         result = haxi_user.HaxiUser.get_news(fields=fields, contions=contions,
#                                               limit=limit, skip=skip, desc=desc)
#         if result:
#             return JsonResponse(data, status=status.HTTP_200_OK)
#         data['status'] = 'error'
#         data['msg'] = '没有新消息'
#         return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def train(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-t_id'
        result = haxi_train.HaxiTrain.get_Train(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        for query in result:
            query['t_createtime'] = time.mktime(query['t_createtime'].timetuple())
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_train.HaxiTrain.create_train(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


# trainmiddle view
@api_view(['GET'])
def train_middle(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-ym_id'
        result = haxi_train_middle.TrainMiddle.get_train_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)


#exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def examine(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-t_id'
        result = haxi_basis.HaxiBasic.get_examine(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get examine failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        for query in result:
            query['e_createtime'] = time.mktime(query['e_createtime'].timetuple())
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_basis.HaxiBasic.create_examine(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


# work view
@api_view(['GET', 'POST', 'UPDATE'])
def work(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else '-t_id'
        result = haxi_basis.HaxiBasic.get_examine(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get examine failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        for query in result:
            query['e_createtime'] = time.mktime(query['e_createtime'].timetuple())
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_basis.HaxiBasic.create_examine(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


