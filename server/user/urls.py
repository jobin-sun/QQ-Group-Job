__author__ = 'jobin'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^list/', views.list),
    url(r'^reg/', views.register),
    url(r'^login/', views.login),
    url(r'^profile/', views.getUserInfo),
    url(r'^change_pwd/', views.changePwd),
]