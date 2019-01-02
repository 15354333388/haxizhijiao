from django.conf.urls import url

from . import views

app_name = '[hzxi]'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^user/homepage/$', views.user_home_page, name='user_home_page'),
    url(r'^admin/homepage/$', views.admin_home_page, name='admin_home_page'),
    url(r'^user/information/$', views.user_information, name='user_information'),
    url(r'^user/manoeuvration/$', views.manoeuvre_information, name='manoeuvre_information'),
    url(r'exam/', views.exam, name='exam'),
    url(r'^$', views.index),
    ]