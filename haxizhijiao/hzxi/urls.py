from django.conf.urls import url

from . import views

app_name = '[hzxi]'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),  # user login account
    url(r'^register/$', views.register, name='register'),  # user register acaount
    url(r'^logout/$', views.logout, name='logout'),  # user logout own account
    url(r'^index/$', views.index, name='index'),  # enter web home page
    # url(r'^user/homepage/$', views.user_home_page, name='user_home_page'),
    # url(r'^admin/homepage/$', views.admin_home_page, name='admin_home_page'),
    url(r'^user/management/$', views.user_management, name='user_management'),
    url(r'^user/manoeuvre/$', views.user_manoeuvre, name='user_manoeuvre'),
    url(r'^user/manoeuvre_middle/$', views.manoeuvre_middle, name='user_manoeuvre_middle'),
    url(r'^user/train/$', views.user_train, name='user_train'),
    url(r'^user/examine/$', views.user_examine, name='user_examine'),
    url(r'^user/work/$', views.user_work, name='user_work'),
    url(r'^incident/$', views.incident),
    url(r'^ceshi',views.ceshi,name='ceshi'),
    url(r'^upload',views.upload, name='upload'),
    url(r'^test/$', views.test),
    url(r'^$', views.index),
    ]