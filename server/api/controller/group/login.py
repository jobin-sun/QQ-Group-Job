

"""
输入:
    {
        "groupId":"xxxx",
        "adminName":"xxxx",
        "password":"xxxx"
    }

保存:
    相关表: modules.GroupAdmin

返回:
    {
        "status":"success",#必需
        "msg":"xxxx",#必需
        ....#可选
    }
"""

from django.http import JsonResponse
from django.views.generic import View

from django.forms import (Form, PasswordInput, CharField )

from .check_request import CheckRequest
from api.models import GroupAdmin
from api import config
import hashlib
import time

class LoginForm(Form):
    groupId = CharField(label=u'群ID：', max_length=15)
    adminName = CharField(label=u'群主QQ：', max_length=15)
    password = CharField(label=u'密码：', widget=PasswordInput())



class Index(View):
    def post(self, request):
        check = CheckRequest(request);
        if check.admin:
            return JsonResponse({"status": 'error',
                        'msg': "User logined"
            })
        uf = LoginForm(check.jsonForm)
        if uf.is_valid():
            groupId = uf.cleaned_data['groupId']
            adminName = uf.cleaned_data['adminName']
            pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
            password = hashlib.sha1(pwd).hexdigest()
            # 获取的表单数据与数据库进行比较
            admin = GroupAdmin.objects.filter(groupId__exact=groupId, adminName__exact=adminName, password__exact=password).first()
            if admin:
                data = {"status": 'success',
                        'msg': "Login success"
                        }

                # 将username写入浏览器cookie,失效时间为3600 * 24 * 30
                now = int(time.time())

                sha1 = hashlib.sha1((admin.random + config.keyToken + str(now)).encode("utf-8")).hexdigest()
                cookieOpt = {'expires': now + config.expiration}
                token = groupId + "-"+ adminName +"-" + str(now) + "-" + sha1

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
                                     'msg': "GroupID or adminName or password is error"
                                     })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error"
                                 })
