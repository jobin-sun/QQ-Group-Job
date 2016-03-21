

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

from django.forms import (Form, PasswordInput, CharField)

from .check_request import CheckRequest
from api.token import new_token, db_password
from api.models import GroupAdmin
from api.config import expiration
from api.error_code import error_code

class LoginForm(Form):
    groupId = CharField(label=u'群ID：', max_length=15)
    qq = CharField(label=u'群主QQ：', max_length=15)
    password = CharField(label=u'密码：', widget=PasswordInput())



class Index(View):
    def post(self, request):
        check = CheckRequest(request);
        uf = LoginForm(check.jsonForm)
        if uf.is_valid():
            groupId = uf.cleaned_data['groupId']
            qq = uf.cleaned_data['qq']
            password = db_password(uf.cleaned_data['password'])

            # 获取的表单数据与数据库进行比较
            admin = GroupAdmin.objects.filter(
                groupId__exact=groupId,
                qq__exact=qq,
                password__exact=password
            ).first()

            if admin:
                if admin.status == 0:
                    return JsonResponse({
                        "status": 'error',
                        "code": 20002,
                        "msg": error_code[20002]
                    })
                data = {
                    "status": 'success',
                    'msg': "Login success"
                }

                admin_token = new_token(admin, 'login')
                token = admin_token.get_token()
                cookieOpt = admin_token.expired_time

                data['cookies'] = {
                    'token': {
                        'value': token,
                        'opt': cookieOpt
                    }
                }
                response = JsonResponse(data)
                response.set_cookie("admin_token",value=token, max_age=expiration['login'], httponly=True)
                response.set_cookie("admin_logined",value="yes", max_age=expiration['login'])
                return response
            else:
                # 用户名或密码错误
                return JsonResponse({"status": 'error',
                                     'msg': "GroupID or qq or password is error"
                                     })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error: %s" % uf.errors
                                 })
