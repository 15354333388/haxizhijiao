from django.conf.urls import url

from . import views

app_name = '[hzxi]'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^$', views.index),
    ]