from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, CharField )

from .check_request import CheckRequest
from api.error_code import error_code

class NickForm(Form):
    nick = CharField(max_length=15)

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "code":20000,
                                "msg": error_code[20000]})

        return JsonResponse({
            "status": "success",
            "msg":"",
            "data":{
                "groupId": check.admin.groupId,
                "qq": check.admin.qq,
                "nick": check.admin.nick,
                "userType": check.admin.userType
            }
        })
    def put(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = NickForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({
                "status" : 'error',
                'msg' : "Illegal put: %s" % uf.errors
            })
        check.admin.nick = uf.cleaned_data['nick']
        check.admin.save()
        return JsonResponse({
            "status": "success",
            "msg":"",
            "data":{
                "groupId": check.admin.groupId,
                "qq": check.admin.qq,
                "nick": check.admin.nick,
                "userType": check.admin.userType
            }
        })