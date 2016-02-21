__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from api.models import Resume
from django.forms import (Form, CharField, EmailField, IntegerField, BooleanField, Textarea)

class GetForm(Form):
    groupId = CharField(label=u'群Id：', max_length=15)

class PostForm(Form):
    email = EmailField(max_length=15)
    groupId = CharField(max_length=15) #所属群
    qq = CharField(max_length=15)
    username = CharField(max_length=50)
    sex = IntegerField()
    age = IntegerField(min_value=15, max_value=100)
    yearsOfWorking = IntegerField(min_value=0, max_value=60)
    school = CharField(max_length=40)
    education = IntegerField()
    content = CharField(widget=Textarea)
    display = BooleanField()



class Index(View):
    def get(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = GetForm(check.jsonForm)
        if uf.is_valid():
            item = Resume.objects.filter(userEmail = check.user.email, groupId = uf.cleaned_data['groupId']).first()
            if item:
                return JsonResponse({
                    "status": 'success',
                    'msg': '',
                    'count': 1,
                    'data':{
                        'email': item.userEmail,
                        "groupId": item.groupId,
                        "username": item.username,
                        "qq": item.qq,
                        'sex': item.sex,
                        'age': item.age,
                        'yearsOfWorking': item.yearsOfWorking,
                        'school': item.school,
                        'education': item.education,
                        "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                        "content": item.content,
                        'display': item.display,
                        "status": item.status
                    }
                })
            else:
                return JsonResponse({"status": 'success',
                                 'msg': "Resume not found",
                                 'count': 0,
                                 'data':{
                                     "email": check.user.email,
                                     "username": check.user.username,
                                     "qq": check.user.qq,
                                     'sex': check.user.sex,
                                     'age': check.user.age,
                                     'yearsOfWorking': check.user.yearsOfWorking,
                                     'school': check.user.school,
                                     'education': check.user.education
                                 }
                            })
        else:
            return JsonResponse({"status": 'error',
                                 'msg': "Form is error"
                                 })
    def post(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = PostForm(check.jsonForm)
        if uf.is_valid():
            resume = Resume();
            resume.userEmail = uf.cleaned_data['email'];

            resume.groupId = uf.cleaned_data['groupId'];
            resume.qq = uf.cleaned_data['qq'];
            resume.username = uf.cleaned_data['username'];

            resume.sex = uf.cleaned_data['sex'];
            resume.age = uf.cleaned_data['age'];
            resume.yearsOfWorking = uf.cleaned_data['yearsOfWorking'];
            resume.school = uf.cleaned_data['school'];
            resume.education = uf.cleaned_data['education'];

            resume.content = uf.cleaned_data['content'];
            resume.display = uf.cleaned_data['display'];
            resume.save()
            if resume.id:
                return JsonResponse({
                    "status" : 'success',
                    'msg' : ""
                    })
            else:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "Post error"
                    })
        else:
            return JsonResponse({
                "status": "error",
                "msg": "From error"
            })


