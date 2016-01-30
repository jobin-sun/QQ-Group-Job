
"""
get:
    输入:
        {
            "groupId":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank, modules.User

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
            "data":[
                "resumeId":11111,
                "groupId":"xxx",
                "username":"xxx",
                "qq":"xxx", //优先使用modules.Resume中的qq
                "lastDate":1400000 , //unix时间戳
                "myRank":12,
                "averageRank":20,
                "content":"xxxxx",
                "status":0|1|2
                ]

        }
put:
    输入:
        {
            "resumeId":111,//必需
            "status":0|1|2,//选
            "myRank":222,//选
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }
delete:
    输入:
        {
            "resumeId":111,//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank

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