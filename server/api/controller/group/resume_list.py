
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
from api.models import Resume, Rank
from .form import MngResumeForm, DelResumeForm


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
        resumes = Resume.objects.filter(groupId__exact = check.admin.groupId, display__exact= True)
        for item in resumes:
            allRank = Rank.objects.filter(resumeId__exact = item.id)
            rank = allRank.filter(qq__exact = check.admin.qq).first()
            avgRank = allRank.aggregate(Avg('rank'))
            resume = {
                "id": item.id,
                "groupId": item.groupId,
                "qq": item.qq,
                "userEmail": item.userEmail,
                "username": item.username,
                "sex": item.sex,
                "age": item.age,
                "yearsOfWorking": item.yearsOfWorking,
                'school': item.school,
                'education': item.education,
                "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                "content": item.content,
                "status": item.status
            }
            if not rank:
                resume['myRank'] = -1
            else:
                resume['myRank'] = rank.rank
            if not avgRank['rank__avg']:
                resume['averageRank'] = -1
            else:
                resume['averageRank'] = avgRank['rank__avg']
            data['data'].append(resume)
        return JsonResponse(data)