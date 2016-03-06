
"""
put:
    输入:
        {
            "password":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.GroupAdmin

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }


"""

from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from .form import PwdForm
from api.token import db_password


class Index(View):

    def put(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "User not logined"})
        uf = PwdForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "Password is invalid."})
        check.admin.password = db_password(uf.cleaned_data['password'])
        check.admin.save()
        return JsonResponse({"status" : "success",
                             "msg" : ""})

