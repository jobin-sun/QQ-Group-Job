from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Avg

from .check_request import CheckRequest
from api.models import Resume, Rank
from .form import MngResumeForm, DelResumeForm
from django.forms import (Form, IntegerField)
from api.error_code import error_code


class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                 "code":20000,
                                 "msg": error_code[20000]})
        uf = DelResumeForm(check.jsonForm)
        if uf.is_valid():
            resume = Resume.objects.filter(id__exact = uf.cleaned_data["resumeId"], display__exact= True).first()
            if resume:
                allRank = Rank.objects.filter(resumeId__exact = uf.cleaned_data["resumeId"],qq__exact = check.admin.qq)
                rank = allRank.filter(qq__exact = check.admin.qq).first()
                avgRank = allRank.aggregate(Avg('rank'))
                myRank = -1
                averageRank = -1
                if rank:
                    myRank = rank.rank
                if avgRank['rank__avg']:
                    averageRank = avgRank['rank__avg']
                return JsonResponse({"status" :  "success",
                    "msg" :  '',
                    "data" : {
                        "id": resume.id,
                        "jobTitle": resume.jobTitle,
                        "groupId": resume.groupId,
                        "qq": resume.qq,
                        "email": resume.userEmail,
                        "username": resume.username,
                        "sex": resume.sex,
                        "age": resume.age,
                        "yearsOfWorking": resume.yearsOfWorking,
                        'school': resume.school,
                        'education': resume.education,
                        "lastDate": resume.lastDate,
                        "content": resume.content,
                        "status": resume.status,
                        "myRank":myRank,
                        "averageRank": averageRank

                    }
                })
            else:
                return JsonResponse({"status": 'error',
                                 'msg': "Resume not found form"
                                 })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "login form is error: %s" % uf.errors
                                 })

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
        resume = Resume.objects.filter(id = uf.cleaned_data['resumeId'],groupId__exact = check.admin.groupId).first()
        if uf.cleaned_data['status']:
            resume.status = uf.cleaned_data['status']
            resume.save()
        if uf.cleaned_data['rank']:
            rank = Rank.objects.filter(resumeId = uf.cleaned_data['resumeId'],qq__exact = check.admin.qq).first()
            if uf.cleaned_data['rank'] == -1:
                if rank:
                    rank.delete()
            else:
                if rank:
                    rank.rank = uf.cleaned_data['rank']
                else:
                    rank = Rank(
                        resumeId = uf.cleaned_data['resumeId'],
                        qq = check.admin.qq,
                        groupId= check.admin.groupId,
                        rank= uf.cleaned_data['rank']

                    )
                rank.save()
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
        Resume.objects.filter(id = uf.cleaned_data['resumeId'],groupId__exact = check.admin.groupId).delete()
        Rank.objects.filter(resumeId = uf.cleaned_data['resumeId'],qq__exact = check.admin.qq).delete()
        return JsonResponse({"status":"success",
                             "msg":""})