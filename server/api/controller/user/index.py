__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from django.forms import Form, PasswordInput, CharField, EmailField, BooleanField, Textarea

from .check_request import CheckRequest
from api.models import Resume


class UserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    password = CharField(label=u'密码：', widget=PasswordInput())
    qq = CharField(label='QQ：', max_length=15)


class UpdateUserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    display = BooleanField(required=False,initial=False)
    content = CharField(label=u'详情',required=False,widget=Textarea)

class Index(View):
    def get(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        data = {"status" :  "success",
                "msg" :  '',
                "data" :  {
                    "username" :  check.user.username,
                    "qq" : check.user.qq,
                    'sex' : check.user.sex,
                    'age' : check.user.age,
                    'yearsOfWorking' : check.user.yearsOfWorking,
                    'school' : check.user.school,
                    'education' : check.user.education,
                    "addDate" :  check.user.addDate.strftime('%Y-%m-%d')
                    }
                }
        resume = Resume.objects.filter(qq__exact = check.user.qq).first()
        if resume:
            data['data'].update({
                "content" : resume.content,
                "display" : resume.display,
                "contentDate" : resume.lastDate.strftime('%Y-%m-%d %H:%m')
                })
        return JsonResponse(data)

    def put(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        uf = UpdateUserForm(check.jsonForm)
        if uf.is_valid():
            check.user.username = uf.cleaned_data['username']
            check.user.save()
            resume = Resume.objects.filter(qq__exact = check.user.qq).first()
            if not resume:
                resume = Resume()
                resume.qq = check.user.qq
            resume.content = uf.cleaned_data['content']
            resume.display = uf.cleaned_data['display']
            resume.save()

            return JsonResponse({"status" : "success",
                    "msg" :  ''
                    })
        else:
            return JsonResponse({"status" : "error",
                    "msg" : 'Illegal put'
                    })
