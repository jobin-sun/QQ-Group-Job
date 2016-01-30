__author__ = 'jobin'

import hashlib
import random
import string

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField, EmailField )

from .check_request import CheckRequest
from api.models import User
from api import config


class UserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    password = CharField(label=u'密码：', widget=PasswordInput())
    qq = CharField(label='QQ：', max_length=15)
    email = EmailField(label=u'电子邮件：')

class Reg(View):
    def post(self, request):
        check = CheckRequest(request);
        if check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User logined"
            })
        uf = UserForm(check.jsonForm)
        if uf.is_valid():
            #检测用户是否存在
            checkUser = User.objects.filter(email__exact = uf.cleaned_data['email']).first()
            if checkUser:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "此Email账户已存在"
                })
            user = User()
            user.username = uf.cleaned_data['username']
            pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
            user.password = hashlib.sha1(pwd).hexdigest()
            user.qq = uf.cleaned_data['qq']
            user.email = uf.cleaned_data['email']
            user.random = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            user.save()

            return JsonResponse({
                "status" : 'success',
                'msg' : ""
            })
        else:
            return JsonResponse({
                "status" : 'error',
                'msg' : "Illegal post"
            })
