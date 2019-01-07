#coding: utf-8
import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from . import permissions
from . import haxi_login
from . import haxi_manoeuvre
from . import haxi_request
from . import haxi_train
# from . import haxi_basis
from . import haxi_maneouvre_middle
from . import haxi_train_middle
from . import database
from . import haxi_user
from . import haxi_work
from . import haxi_examine_bank
# Create your views here.


# index，if not login, must login in index, only and receive method of 'get'
# checked session, if user has login, it will redirect own page
# @permissions.is_login
@api_view(['GET'])
def index(request):
    # if request.COOKIES.get('is_login', False):
    #     try:
    #         query = models.User.objects.get(u_pid=request.session.get('pid'))
    #         if query.u_permission == '3':
    #             return redirect('/hzxi/user/homepage/')
    #         elif query.u_permission == '2':
    #             return redirect('/hzxi/admin/homepage/')
    #     except models.User.DoesNotExist or models.User.MultipleObjectsReturned:
    #         pass
    return render(request, 'index1.html')


@api_view(['GET'])
# @permissions.is_login
# def user_home_page(request):
#     return render(request, 'personal.html')
#
#
# @api_view(['GET'])
# # @permissions.is_login
# def admin_home_page(request):
#     return render(request, '#')
# finish user login, only receive method of 'post'
# @permissions.verify_permission # check permissions
@api_view(['POST'])
def login(request):
    return haxi_login.HaxiLogin.login(request)


# finsih user register, only receive method of 'post'
@api_view(['POST', 'GET'])
def register(request):
    return haxi_login.HaxiLogin.register(request)


# logout user
# @permissions.is_login
@api_view(['POST'])
def logout(request):
    return haxi_login.HaxiLogin.logout(request)


# finish user's information
# @permissions.is_login
# @permissions.is_same
@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
@permissions.is_ajax
def user_management(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        if not body['fields']:
            fields = database.user_fields.copy()
            fields.remove('u_pwd')
            body['fields'] = fields
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'u_id'
        result = haxi_user.User.get(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = result
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        informations = body.get('Informations')
        if not (informations and type(informations) == list):
            data['status'] = 'error'
            data['msg'] = 'new user is lack of contions, or bad request'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_user.User.create(informations)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part users have created, but index is %s error' % result
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data, status==status.HTTP_201_CREATED)

    elif request.method == 'UPDATE':
        body = json.loads(request.body.decode(encoding='utf-8'))
        updateDate = body.get('updateDate')
        if not (type(updateDate) == list and updateDate):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_user.User.update(updateDate)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part update have created, but index is %s error' % result
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        body = request.body.decode(encoding='utf-8')
        contions = body.get('contions')
        if not (contions and type(contions) == []):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_user.User.delete(contions)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part user have delete, but index is %s error' % result
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(data, status=status.HTTP_200_OK)


# user_Manoeuvre view
# @permissions.is_login
@api_view(['GET', 'POST', 'UPDATE'])
@permissions.is_ajax
def user_manoeuvre(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'y_id'
        body['fields'] = body['fields'] if body['fields'] else database.manoeuvre_fields
        result = haxi_manoeuvre.Manoeuvre.get_manoevure(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get manoeuver failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        data['data'] = result
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create manoeuver failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_manoeuvre.Manoeuvre.create_manoeuvre(contents)
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
        result = haxi_manoeuvre.Manoeuvre.update_manoeuvre(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_200_OK)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


# manoeuvre_middle view
@api_view(['GET'])
def manoeuvre_middle(request):
    data = {
        'status': 'OK',
        'msg': '',
        'data': ''
    }
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'ym_id'
        result = haxi_maneouvre_middle.ManeouvreMiddle.get_maneouvre_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)


# user_train
@api_view(['GET', 'POST', 'UPDATE'])
def user_train(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 't_id'
        body['fields'] = body['fields'] if body['fields'] else database.train_fields
        result = haxi_train.Train.get_train(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        data['data'] = result
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_train.Train.create_train(contents)
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
            data['msg'] = 'create train failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_train.Train.update_train(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_200_OK)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

# train_middle view
@api_view(['GET'])
def train_middle(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'ym_id'
        result = haxi_train_middle.TrainMiddle.get_train_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        data['data'] = [query for query in result]
        return JsonResponse(data, status=status.HTTP_200_OK)


# user_exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def user_examine(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'e_id'
        body['fields'] = body['fields'] if body['fields'] else database.examine_fields
        result = haxi_examine_bank.Examine.get_examine(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        data['data'] = result
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create examine failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_examine_bank.Examine.create_examine(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'UPDATE':  # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create examine failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_examine_bank.Examine.update_examine(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_200_OK)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


# user_work view
@api_view(['GET', 'POST', 'UPDATE'])
def user_work(request):
    data = database.data.copy()
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'e_id'
        body['fields'] = body['fields'] if body['fields'] else database.examine_fields
        result = haxi_work.Work.get_work(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        data['data'] = result
        return JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create work failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_work.Work.create_work(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'UPDATE':  # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create work failed, because data type is error'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_work.Work.update_work(contents)
        if not result:
            return JsonResponse(data, status=status.HTTP_200_OK)
        data['status'] = 'error'
        data['msg'] = result
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


