__author__ = 'jobin'

import hashlib

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField )

from .check_request import CheckRequest
from api import config


class PwdForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())

class ChangePwd(View):
    def put(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = PwdForm(check.jsonForm)
        if uf.is_valid():
            pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
            check.user.password = hashlib.sha1(pwd).hexdigest()
            check.user.save()
            return JsonResponse({"status" :  'success',
                    'msg' :  ''
                    })
