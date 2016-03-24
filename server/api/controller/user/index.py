__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from django.forms import Form, IntegerField, CharField

from .check_request import CheckRequest
from api.response_code import errorCode


class UpdateUserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    sex = IntegerField()
    age = IntegerField(min_value=15, max_value=100)
    yearsOfWorking = IntegerField(min_value=0, max_value=60)
    school = CharField(max_length=40)
    education = IntegerField()

class Index(View):
    def get(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "code":10000,
                "msg": errorCode[10000]
            })
        return JsonResponse({"status" :  "success",
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
                })

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
            check.user.sex = uf.cleaned_data['sex']
            check.user.age = uf.cleaned_data['age']
            check.user.yearsOfWorking = uf.cleaned_data['yearsOfWorking']
            check.user.school = uf.cleaned_data['school']
            check.user.education = uf.cleaned_data['education']
            check.user.save()

            return JsonResponse({"status" : "success",
                    "msg" :  ''
                    })
        else:
            return JsonResponse({"status" : "error",
                    "msg" : 'Illegal put: %s' % uf.errors
                    })
