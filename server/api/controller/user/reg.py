__author__ = 'jobin'

import hashlib
import random
import string

from django.http import JsonResponse
from django.views.generic import View
from django.forms import Form, PasswordInput, CharField, EmailField

from .check_request import CheckRequest
from api.models import User
from api.token import db_password, new_random

class UserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    password = CharField(label=u'密码：', widget=PasswordInput(), max_length=40)
    qq = CharField(label='QQ：', max_length=15)

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
            checkUser = User.objects.filter(qq__exact = uf.cleaned_data['qq']).first()
            if checkUser:
                if checkUser.status == 0:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "此qq账户已注册,但未激活"
                    })
                else:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "此qq账户已存在"
                    })

            user = User(
                username = uf.cleaned_data['username'],
                password = db_password(uf.cleaned_data['password']),
                qq = uf.cleaned_data['qq'],
                login_random = new_random(),
                activate_random = new_random(),
                recover_random = new_random()
            )
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
