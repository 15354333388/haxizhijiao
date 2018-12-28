from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from . import permissions
from . import models
# Create your views here.


# index，if not login, must login in index, only and receive method of 'get'
@api_view(['GET'])
# checked session, if user has login, it will redirect own page
# @permissions.is_login
def index(request):
    return render(request, 'index1.html')


# finish user login, only receive method of 'post'
@api_view(['POST'])
# @permissions.verify_permission # check permissions
def login(request):
    return HttpResponse('sss')
# finsih user register, only receive method of 'post'
@api_view(['POST', 'GET'])
def register(request):
    print(request.get_host())
    print('qawsqaws')
    data = {
        'status': 'OK',
        'data': ''
    }
    print('1234')
    if request.method == 'GET':
        u_pid = str(request.GET.get('u_pid', ''))
        print(u_pid)
        if u_pid:
           u_name = models.User.objects.get(u_pid=u_pid).u_name
           data['u_name'] = u_name
        else:
            data['status'] = 'error'
        return JsonResponse(data)
    if request.method == 'POST':
        print('54321')
        u_pid = request.POST.get('u_pid', '')
        u_name = request.POST.get('u_name', '')
        query = models.User.objects.get(u_name=u_name, u_pid=u_pid)
        print(request.POST.get('u_pwd', ''))
        query.u_pwd = request.POST.get('u_pwd', '')
        query.save()
    return JsonResponse(data)
    # return redirect('')
    #
    # return HttpResponse('Register')


# finish user update informations, only receive method of 'update'
@api_view(['UPDATE'])
def update(request):
    pass


#exam funcation
@api_view(['GET', 'POST', 'UPDATE'])
def exam(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass