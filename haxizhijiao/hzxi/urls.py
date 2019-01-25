from django.conf.urls import url
from . import views

app_name = '[hzxi]'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),  # user login account
    url(r'^register/$', views.register, name='register'),  # user register acaount
    url(r'^logout/$', views.logout, name='logout'),  # user logout own account
    url(r'^index/$', views.index, name='index'),  # enter web home page
    url(r'^user/management/$', views.user_management, name='user_management'),  # manoeuvre module
    url(r'^user/manoeuvre/$', views.user_manoeuvre, name='user_manoeuvre'),  # user module
    url(r'^index/manoeuvre/$', views.manoeuvre_index, name='manoeuvre_index'),  # enter manoeuvre home page
    url(r'^manoeuvre/information/$', views.manoeuvre_information, name='manoeuvre_information'),  # show manoeuvre message
    url(r'^user/center/$', views.user_center, name='user_center'),  # enter user home page
    url(r'^user/manoeuvre_middle/$', views.manoeuvre_middle, name='user_manoeuvre_middle'),  # manoeuvre record module
    url(r'^user/train/$', views.user_train, name='user_train'),  # train module
    url(r'^user/echo/$', views.echo, name='echo'),  # user communication and message send
    url(r'^user/examine/$', views.user_examine, name='user_examine'),  # examine module
    url(r'^user/work/$', views.user_work, name='user_work'),  # work module
    url(r'^incident/$', views.incident),  # all function record
    url(r'^message/$', views.message),  # all function record
    url(r'^$', views.index),  # web home page
    ]