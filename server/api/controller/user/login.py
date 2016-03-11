__author__ = 'jobin'

import hashlib

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField, EmailField)

from .check_request import CheckRequest
from api.token import new_token
from api.models import User
from api.token import db_password
from api.config import expiration

class LoginForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())
    qq = CharField(label='QQ：', max_length=15)


class Login(View):
    def post(self, request):
        check = CheckRequest(request);
        uf = LoginForm(check.jsonForm)
        if uf.is_valid():
            qq = uf.cleaned_data['qq']
            password = db_password(uf.cleaned_data['password'])
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(qq__exact=qq, password__exact=password).first()
            if user:
                if user.status == 1:
                    data = {"status": 'success',
                            'msg': "Login success"
                            }

                    user_token = new_token(user, 'login')
                    token = user_token.get_token()
                    cookieOpt = user_token.expired_time

                    data['cookies'] = {
                        'token': {
                            'value': token,
                            'opt': cookieOpt
                        }
                    }
                    response = JsonResponse(data)
                    response.set_cookie("token", value=token, max_age=expiration['login'], httponly=True)
                    response.set_cookie("logined", value="yes", max_age=expiration['login'])
                    return response
                elif user.status == 0:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "此qq账户已注册,但未激活"
                    })
                else:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "用户状态不合法，请联系管理员"
                    })
            else:
                # 用户名或密码错误
                return JsonResponse({"status": 'error',
                                     'msg': "email or password is error"
                                     })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error"
                                 })
