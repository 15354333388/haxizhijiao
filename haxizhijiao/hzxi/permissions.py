# coding: utf-8
# 2018-12-28 9:15
import json
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from . import models
from . import database


def is_login(func):
    def wapper(request, *args, **kwargs):
        if request.COOKIES.get('is_login', False):
            u_pid = request.session.get('pid', '')
            query = models.User.objects.filter(u_pid=u_pid)
            if query and len(query) == 1:
                return func(request, *args, **kwargs)
            else:
                return redirect('/hzxi/index/')
        else:
            return redirect('/hzxi/index/')
    return wapper

def verify_permissions(func):
    def wapper(request, *args, **kwargs):
        func(request, *args, **kwargs)
    return wapper


def is_ajax(func):
    def wapper(request, *args, **kwargs):
        if not request.is_ajax():
            data = database.data
            data['status'] = 'error'
            data['msg'] = 'only receive ajax request'
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        return func(request, *args, **kwargs)
    return wapper


def is_same(func):
    def wapper(request, *args, **kwargs):
        data = database.data
        data['status'] = 'error'
        data['msg'] = 'session is not same request, please login again'
        if request.method == 'GET':
            if not (json.loads(request.GET.get('u_pid')) if request.GET.get('u_pid') else None == request.session['pid']):
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        elif not request.body.get('u_pid') == request.session['pid']:
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        print('ok------------------', request.path, request.method)
        return func(request, *args, **kwargs)
    return wapper