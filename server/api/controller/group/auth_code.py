
"""
get:
    输入:
        {
            "groupId":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.AuthCode

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
            "data":[
                "id":111,
                "adminName":11111,
                "code":"xxx",
                "times":2222
                ]

        }
post:
    输入:
        {
            "code":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.AuthCode

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需

        }
delete:
    输入:
        {
            "id":111,//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.AuthCode

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }

"""

from django.http import JsonResponse
from django.views.generic import View

import time

from .check_request import CheckRequest
from .form import AuthCodeForm, DelAuthCodeForm
from api.models import AuthCode

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        if check.admin.userType == 1:
            codes = AuthCode.objects.filter(groupId__exact = check.admin.groupId).values('id', 'qq', 'code', 'times')
        else:
            codes = AuthCode.objects.filter(groupId__exact = check.admin.groupId, qq__exact=check.admin.qq).values('id', 'qq', 'code', 'times')
        data = {"status" : "success",
                "msg":"",
                "data": [] }
        for item in codes:
            data["data"].append(item)
        return JsonResponse(data)

    def post(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = AuthCodeForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "Illegal AuthCode."})
        rst = AuthCode.objects.filter(groupId__exact = check.admin.groupId, code__exact=uf.cleaned_data['code']).count()
        print(rst)
        if rst != 0:
            return JsonResponse({"status" : "error",
                                "msg" : "Auth code exist."})

        code = AuthCode(
            groupId=check.admin.groupId,
            qq=check.admin.qq,
            code=uf.cleaned_data['code'],
            times=0,
            lastDate=time.time()
            )
        code.save()
        return JsonResponse({"status":"success",
                             "msg":"Update Success.",
                             "data":{
                                 "id":code.id,
                                 "qq":code.qq,
                                 "code":code.code,
                                 "times": code.times
                             }})

    def put(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})

    def delete(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = DelAuthCodeForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "AuthCodeId is invalid."})
        code = AuthCode.objects.filter(id = uf.cleaned_data['id']).first()
        if not code:
            return JsonResponse({"status" : "error",
                                "msg" : "No such code."})
        code.delete()
        return JsonResponse({"status" : "success",
                             "msg" : "Delete success."})
