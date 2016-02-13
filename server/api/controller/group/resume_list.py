
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
from django.db.models import Avg

from .check_request import CheckRequest
from api.models import Resume, Rank, User
from .form import (MngResumeForm, DelResumeForm)


class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
        data = {"status" :  "success",
                "msg" :  '',
                "data" : []
                }
        resumes = Resume.objects.filter(groupId = check.admin.groupId)
        for item in resumes:
            user = User.objects.filter(email = item.userEmail).first()
            allRank = Rank.objects.filter(resumeId = item.id)
            rank = allRank.filter(adminName = check.admin.adminName).first()
            avgRank = allRank.aggregate(Avg('rank'))
            if not user:
                return JsonResponse({"status": "error",
                                    "msg": "Resume without valid user"})
            resume = {
                "resumeId": item.id,
                "groupId": item.groupId,
                "username": user.username,
                "qq": item.qq,
                "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                "content": item.content,
                "status": item.status
            }
            if not rank: 
                resume['myRank'] = u'尚未评分'
            else:
                resume['myRank'] = rank.rank
            resume['averageRank'] = avgRank['rank__avg']
            data['data'].append(resume)
        return JsonResponse(data)
        
    def post(self, request):
        return JsonResponse({"status":"success",
                             "msg":""})

    def put(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
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
        return JsonResponse({"status":"success",
                             "msg":""})

    def delete(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                "msg": "Only admin permitted"})
        uf = DelResumeForm(check.jsonForm)
        if not uf.is_valid():
            return JsonResponse({"status": "error",
                                "msg": "resumeId is invalid."})
        Resume.objects.filter(id = uf.cleaned_data['resumeId']).delete()
        Rank.objects.filter(resumeId = uf.cleaned_data['resumeId']).delete()
        return JsonResponse({"status":"success",
                             "msg":""})