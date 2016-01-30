__author__ = 'jobin'

import hashlib
import time
import base64

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField, EmailField)

from .check_request import CheckRequest
from api.models import User
from api import config


class LoginForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())
    email = EmailField(label=u'电子邮件：')



class Login(View):
    def post(self, request):
        check = CheckRequest(request);
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

                # 将username写入浏览器cookie,失效时间为3600 * 24 * 30
                now = int(time.time())

                sha1 = hashlib.sha1((user.random + config.keyToken + str(now)).encode("utf-8")).hexdigest()
                cookieOpt = {'expires': now + config.expiration}
                token = base64.b64encode(email.encode('utf-8')).decode("utf-8") + "-" + str(now) + "-" + sha1
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
                # 比较失败，还在login
                return JsonResponse({"status": 'error',
                                     'msg': "email or password is error"
                                     })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error"
                                 })
