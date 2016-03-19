
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
                "id":111,
                "adminName":"xxx",
                "groupId":"xxx",
                "userType":1|2|3
                ]

        }
post:
    输入:
        {
            "adminName":'xxx',//必需
            "password":'xxx'//必需
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
put:
    输入:
        {
            "adminName":'xxx',//必需
            "password":'xxx'//必需
            "ResumeId" : //必需，管理管理员简历
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
delete:
    输入:
        {
            "id":'xxx',//必需
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
from .form import CheckAdminForm, DelAdminForm, MngResumeForm
from api.models import GroupAdmin, Resume, User
from api.token import db_password, new_random

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin or check.admin.userType != 1:
            return JsonResponse({"status" : "error",
                                "msg" : "只有群主才有权限"})
        admins = GroupAdmin.objects.filter(
            groupId = check.admin.groupId,
            userType = 0
        ).values('id', 'groupId','nick', 'qq', 'status')

        data = {"status" : "success",
                "msg":"",
                "data": [] }
        for admin in admins:
            data["data"].append(admin)
        return JsonResponse(data)

    def post(self, request):
        ''' 群主添加新管理员 '''
        check = CheckRequest(request)
        if not check.admin or check.admin.userType != 1:
            return JsonResponse({"status" : "error",
                                "msg" : "只有群主才有权限"})
        uf = CheckAdminForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "Admin is invalid."})
        admin = GroupAdmin.objects.filter(
            groupId = check.admin.groupId,
            qq = uf.cleaned_data['qq'],
        ).first()
        if admin:
            return JsonResponse({"status": 'error',
                                'msg': "Admin exist."})
        admin = GroupAdmin(
            groupId=check.admin.groupId,
            qq=uf.cleaned_data['qq'],
            nick=uf.cleaned_data['nick'],
            password = db_password(new_random()),
            login_random = new_random(),
            userType=0
            )
        admin.save()
        return JsonResponse({"status" : "success",
                             "msg" : "Update success.",
                             "data":{
                                 "id": admin.id,
                                 "groupId": admin.groupId,
                                 "nick": admin.nick,
                                 "qq": admin.qq,
                                 "status": admin.status
                             }})

    def delete(self, request):
        check = CheckRequest(request)
        if not check.admin or check.admin.userType != 1:
            return JsonResponse({"status" : "error",
                                "msg" : "只有群主才有权限"})
        uf = DelAdminForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "GroupAdminId is invalid."})
        admin = GroupAdmin.objects.filter(id = uf.cleaned_data['id'], groupId__exact=check.admin.groupId).first()
        if not admin:
            return JsonResponse({"status" : "error",
                                "msg" : "No such admin."})
        admin.delete()
        return JsonResponse({"status" : "success",
                             "msg" : "Delete success."})
