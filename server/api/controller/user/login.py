__author__ = 'jobin'

import hashlib

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField, EmailField)

from .check_request import CheckRequest
from api.token import new_userToken
from api.models import User
from api import config


class LoginForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())
    email = EmailField(label=u'电子邮件：')



class Login(View):
    def post(self, request):
        check = CheckRequest(request);
        if check.user:
            return JsonResponse({"status": 'error',
                        'msg': "User logined"
                        })
        uf = LoginForm(check.jsonForm)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
            password = hashlib.sha1(pwd).hexdigest()
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(email__exact=email, password__exact=password).first()
            if user:
                data = {"status": 'success',
                        'msg': "Login success"
                        }

                user_token = new_userToken(user)
                token = user_token.get_token()
                cookieOpt = user_token.expired_time

                data['cookies'] = {
                    'token': {
                        'value': token,
                        'opt': cookieOpt
                    }
                }
                response = JsonResponse(data)
                response.set_cookie("token",value=token, max_age=config.expiration, httponly=True)
                return response
            else:
                # 用户名或密码错误
                return JsonResponse({"status": 'error',
                                     'msg': "email or password is error"
                                     })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error"
                                 })
