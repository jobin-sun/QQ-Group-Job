
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

import hashlib, random, string

from .check_request import CheckRequest
from .form import CheckAdminForm, DelAdminForm, MngResumeForm
from api.models import GroupAdmin, Resume, User
from api import config

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        admins = GroupAdmin.objects.filter(groupID = check.admin.groupID, userType = 0).values('id','groupID','adminName')
        data = {"status" : "success",
                "msg":"",
                "data": [] }
        for item in admins:
            admin = User.objects.filter(username = item['adminName']).first()
            resume = Resume.objects.filter(groupID = check.admin.groupID, userEmail = admin.email).first()
            if resume:
                item['status'] = resume.status
            else:
                item['status'] = '尚无简历'
            data["data"].append(item)
        return JsonResponse(data)

    def post(self, request):
        ''' 群主添加新管理员 '''
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = CheckAdminForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "Admin is invalid."})
        pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
        password = hashlib.sha1(pwd).hexdigest()
        admin = GroupAdmin.objects.filter(groupID = check.admin.groupID, adminName = uf.cleaned_data['adminName'], password = password).first()
        if admin:
            return JsonResponse({"status": 'error',
                                'msg': "Admin exist."})
        rdm = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        admin = GroupAdmin.create(check.admin.groupID, uf.cleaned_data['adminName'], password, rdm, 0)
        admin.save()
        return JsonResponse({"status" : "success",
                             "msg" : "Update success."})

    def put(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = CheckAdminForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "Admin is invalid."})
        pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
        password = hashlib.sha1(pwd).hexdigest()
        admin = GroupAdmin.objects.filter(groupID = check.admin.groupID, adminName = uf.cleaned_data['adminName'], password = password).first()
        if not admin:
            return JsonResponse({"status": 'error',
                                'msg': "GroupID or adminName or password is error"})
        uf = MngResumeForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status": "error",
                                "msg": "resumeId is invalid."})
        resume = Resume.objects.filter(id = uf.cleaned_data['resumeId']).first()
        if uf.cleaned_data['status']:
            resume.status = uf.cleaned_data['status']
        if uf.cleaned_data['rank']:
            resume.rank = uf.cleaned_data['rank']
        resume.save()
        return JsonResponse({"status" : "success",
                             "msg" : "Update success."})

    def delete(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})
        uf = DelAdminForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status" : "error",
                                "msg" : "GroupAdminId is invalid."})
        admin = GroupAdmin.objects.filter(id = uf.cleaned_data['Id']).first()
        if not admin:
            return JsonResponse({"status" : "error",
                                "msg" : "No such admin."})
        GroupAdmin.objects.filter(id = uf.cleaned_data['Id']).delete()
        return JsonResponse({"status" : "success",
                             "msg" : "Delete success."})