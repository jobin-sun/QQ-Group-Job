
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

class Index(View):
    def get(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})
    def post(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})

    def put(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})
    def delete(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})