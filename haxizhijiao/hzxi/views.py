# -*- coding: utf-8 -*-
import json
import copy
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from . import haxi_incident
from . import permissions
from . import haxi_login
from . import haxi_manoeuvre
from . import haxi_request
from . import haxi_train
from . import haxi_maneouvre_middle
from . import haxi_train_middle
from . import database
from . import haxi_user
from . import haxi_work
from . import haxi_examine_bank
from . import models
from . import haxi_message

# Create your views here.

clients = dict()

# index，if not login, must login in index, only and receive method of 'get'
# checked session, if user has login, it will redirect own page
# @permissions.is_login


def CRS(res):  # 后端解决ajax跨域
    res['Access-Control-Allow-Origin'] = "*"
    return res


def OPTION():  # 解决跨域非简单请求
    body = dict()
    res = JsonResponse(body, status=status.HTTP_204_NO_CONTENT)
    res = CRS(res)


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
    return render(request, 'index.html')
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


@api_view(['GET', 'POST'])
def login(request):
    return haxi_login.HaxiLogin.login(request)


# finish user register, only receive method of 'post'
@api_view(['POST', 'GET'])
def register(request):
    return haxi_login.HaxiLogin.register(request)


# logout user
# @permissions.is_login
@api_view(['POST', 'GET'])
def logout(request):
    return haxi_login.HaxiLogin.logout(request, clients)


# finish user's information
# @permissions.is_login
# @permissions.is_same
@api_view(['GET', 'POST', 'UPDATE', 'DELETE', 'OPTIONS'])
# @permissions.is_ajax
def user_management(request):
    data = copy.deepcopy(database.data)
    if request.method == 'OPTIONS':
        res = OPTION()
        res['Access-Control-Allow-Methods'] = "POST, GET, DELETE, UPDATE, OPTIONS"
        return res
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        if not body['fields']:
            fields = database.user_fields.copy()
            fields.remove('u_pwd')
            body['fields'] = fields
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'u_id'
        print(body)
        result = haxi_user.User.get(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            res = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return CRS(res)
        data['data'] = result
        res = JsonResponse(data, status=status.HTTP_200_OK)
        return CRS(res)
    
    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        informations = body.get('Informations')
        if not (informations and type(informations) == list):
            data['status'] = 'error'
            data['msg'] = 'new user is lack of contions, or bad request'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        result = haxi_user.User.create(informations)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part users have created, but index is %s error' % result
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        else:
            res = JsonResponse(data, status==status.HTTP_201_CREATED)
            return CRS(res)

    elif request.method == 'UPDATE':
        body = json.loads(request.body.decode(encoding='utf-8'))
        print(body)
        update = body.get('update')
        if not (type(update) == list and update):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        result = haxi_user.User.update(update)
        if isinstance(result, int):
            data['status'] = 'error'
            data['msg'] = 'part update have created, but index is %s error' % result
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        res = JsonResponse(data, status=status.HTTP_201_CREATED)
        return CRS(res)

    elif request.method == 'DELETE':
        body = request.body.decode(encoding='utf-8')
        contions = body.get('contions')
        if not (contions and type(contions) == []):
            data['status'] = 'error'
            data['msg'] = 'update date type is error'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        result = haxi_user.User.delete(contions)
        if result:
            data['status'] = 'error'
            data['msg'] = 'part user have delete, but index is %s error' % result
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
    # res = JsonResponse(data, status=status.HTTP_200_OK)
    # return CRS(res)


# user_Manoeuvre view
# @permissions.is_login
@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
# @permissions.is_ajax
def user_manoeuvre(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'y_id'
        if body['contions'].get('y_finished'):
            body['contions']['y_finished'] = int(body['contions']['y_finished'])
        body['fields'] = body['fields'] if body['fields'] else database.manoeuvre_fields
        result = haxi_manoeuvre.Manoeuvre.get_manoevure(body)
        if not result:
            data['data'] = []
            data['status'] = 'error'
            data['msg'] = 'not found manoeuvre'
            res = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
        else:
            data['data'] = result
            res = JsonResponse(data, status=status.HTTP_200_OK)
        return CRS(res)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create manoeuvre failed, because data type is error'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        result = haxi_manoeuvre.Manoeuvre.create_manoeuvre(contents)
        if not isinstance(result, list):
            data['status'] = 'error'
            data['msg'] = 'index %s is error' % result
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        #  send message
        data['data'] = result
        res = JsonResponse(data, status=status.HTTP_200_OK)
        return CRS(res)

    elif request.method == 'UPDATE': # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create manoeuvre failed, because data type is error'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return CRS(res)
        result = haxi_manoeuvre.Manoeuvre.update_manoeuvre(contents)
        if not result:
            res = JsonResponse(data, status=status.HTTP_200_OK)
            return CRS(res)
        data['status'] = 'error'
        data['msg'] = result
        res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return CRS(res)


# manoeuvre home page
def manoeuvre_index(request):
    return render(request, 'drill.html')


#  show single manoeuvre message
def manoeuvre_information(request):
    return render(request, 'exercisedetails.html')


#  show user information
def user_center(request):
    return  render(request, 'personal.html')


# manoeuvre_middle view
@api_view(['GET', 'POST'])
def manoeuvre_middle(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'ym_id'
        if not body['fields']:
            body['fields'] = database.manoeuvre_middle_fields
        result = haxi_maneouvre_middle.ManeouvreMiddle.get_maneouvre_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            res = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return CRS(res)
        data['data'] = [query for query in result]
        res = JsonResponse(data, status=status.HTTP_200_OK)
        return CRS(res)

    if request.method == 'POST':
        body = request.POST
        d = dict()
        d['u_id'], d['y_id'] = int(body.get('u_id')), int(body.get('y_id'))
        text = str(body.get('words'))
        result = haxi_maneouvre_middle.ManeouvreMiddle.create_middle_manoeuvre(d, request.FILES, text=text)
        if isinstance(result, int):
            data['status'] = 'error'
            data['msg'] = result
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            res['Access-Control-Allow-Origin'] = "*"
            return res
        data['data'] = result
        res = JsonResponse(data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = "*"
        return res


# user_train
@api_view(['GET', 'POST', 'UPDATE'])
def user_train(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 't_id'
        body['fields'] = body['fields'] if body['fields'] else database.train_fields
        result = haxi_train.Train.get_train(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        data['data'] = result
        res = JsonResponse(data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            res = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        result = haxi_train.Train.create_train(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_201_CREATED))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return res

    elif request.method == 'UPDATE': # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create train failed, because data type is error'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return  res
        result = haxi_train.Train.update_train(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return  res

# train_middle view
@api_view(['GET'])
def train_middle(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'ym_id'
        result = haxi_train_middle.TrainMiddle.get_train_middle(**body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'user not found'
            res = CRS(JsonResponse(data, status=status.HTTP_404_NOT_FOUND))
            return res
        data['data'] = [query for query in result]
        res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
        return res



# user_exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def user_examine(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'e_id'
        body['fields'] = body['fields'] if body['fields'] else database.examine_fields
        result = haxi_examine_bank.Examine.get_examine(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        data['data'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
        return res

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create examine failed, because data type is error'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        result = haxi_examine_bank.Examine.create_examine(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_201_CREATED))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return res

    elif request.method == 'UPDATE':  # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create examine failed, because data type is error'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        result = haxi_examine_bank.Examine.update_examine(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return res


# user_work view
@api_view(['GET', 'POST', 'UPDATE'])
def user_work(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'e_id'
        body['fields'] = body['fields'] if body['fields'] else database.examine_fields
        result = haxi_work.Work.get_work(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'get train failed'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        data['data'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
        return res

    elif request.method == 'POST':
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == list):
            data['status'] = 'error'
            data['msg'] = 'create work failed, because data type is error'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        result = haxi_work.Work.create_work(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_201_CREATED))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return res

    elif request.method == 'UPDATE':  # user send manoeuvre answer.
        body = json.loads(request.body.decode(encoding='utf-8'))
        contents = body.get('contents')
        if not (contents and type(contents) == dict):
            data['status'] = 'error'
            data['msg'] = 'create work failed, because data type is error'
            res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
            return res
        result = haxi_work.Work.update_work(contents)
        if not result:
            res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
            return res
        data['status'] = 'error'
        data['msg'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_400_BAD_REQUEST))
        return res


def incident(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'i_id'
        body['fields'] = body['fields'] if body['fields'] else database.incident_fields
        result = haxi_incident.Incident.get_incident(body)
        if not result:
            data['status'] = 'error'
            data['msg'] = 'not found incident'
            res = CRS(JsonResponse(data, status=status.HTTP_404_NOT_FOUND))
            return res
        data['data'] = result
        res = CRS(JsonResponse(data, status=status.HTTP_200_OK))
        return res


@accept_websocket
def echo(request):
    def get_message(user_id, message_type=None):
        query_set = list()
        print(user_id, message_type)
        if message_type == 'message':
            queryset = models.Message.objects.filter(m_receive=user_id, m_is_send=0).values('m_symbol', 'm_type')
            for query in queryset:
                l = haxi_manoeuvre.Manoeuvre.get_manoevure({'contions': {'y_id': query['m_symbol']}, 'fields': database.manoeuvre_fields})
                query_set += l
            models.Message.objects.filter(m_receive=user_id, m_is_send=0).update(m_is_send=1)
        elif message_type == 'chat':
            query_set = models.Chat.objects.filter(c_receive=user_id, c_is_send=0).values('c_content')
            if query_set:
                print(query_set)
                query_set = [query for query in query_set]
            models.Chat.objects.filter(c_receive=user_id, c_is_send=0).update(c_is_send=1)
        return query_set
    id = int(request.GET.get('id'))
    # check is  or not login
    if not clients.get(id):
        clients[id] = request.websocket
    # first login, but it  has message.
    chat = get_message(id, message_type='chat')
    information = get_message(id, message_type='message')
    send_data = dict()
    if chat:
        send_data['chat'] = chat
    if information:
        send_data['information'] = information
    if send_data:
        clients[id].send(json.dumps(send_data))
    for message in request.websocket:
        print(message)
        if message == None:
            break
        message = json.loads(message)
        to_id = int(message['to_id'])
        chat = str(message.get('data'))
        information = message.get('information')
        to_send = int(message['to_send'])
        send_data = dict()
        print(information)
        m_body = {
            'm_send': to_id,
            'm_receive': to_send,
            'm_type': information['type'],
            'm_symbol': int(information['y_id']),
        }
        c_body = {
            'c_send': to_id,
            'c_receive': to_send,
            'c_content': chat,
        }
        if chat:
            models.Chat.objects.create(**c_body)
        if information:
            models.Message.objects.create(**m_body)
        if clients.get(to_send):
            data = get_message(to_send, message_type='chat')
            information = get_message(to_send, message_type='message')
            if data:
                send_data['chat'] = data
            if information:
                send_data['information'] = information
            clients[to_send].send(json.dumps(send_data))  # 发送消息到客户端
        else:
            request.websocket.send('send success, but receive is logout，'.encode('utf-8'))


@api_view(['GET', 'POST', 'UPDATE'])
def message(request):
    data = copy.deepcopy(database.data)
    if request.method == 'GET':
        print(request.GET)
        body = haxi_request.HaxiRequest.get_request_contions(request)
        body['desc'] = json.loads(request.GET.get('desc')) if request.GET.get('desc') else 'm_id'
        body['fields'] = body['fields'] if body['fields'] else database.message_fields
        result = haxi_message.Message.get_message(body)
        if not result:
            data['error'] = 'status'
            data['msg'] = 'not found manoeuvre'
            return CRS(JsonResponse(data, status=status.HTTP_404_NOT_FOUND))
        data['data'] = result
        return CRS(JsonResponse(data, status=status.HTTP_200_OK))

# @require_websocket
# def echo_once(request):
#     id = int(request.GET.get('u_id'))
#     message = clients[id].wait()
#     request.websocket.send(message)


# @accept_websocket
# def message(request):
#     if not request.is_websocket():
#         pass
#     if request.method == 'GET':
#         u_id = request.GET.get('u_id')
#         if u_id in clients:







