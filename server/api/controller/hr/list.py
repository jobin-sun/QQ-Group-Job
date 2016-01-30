__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from api.models import AuthCode, Resume



from django.forms import (Form, IntegerField)


class AuthCodeForm(Form):
    code = IntegerField(min_value=100000, max_value=999999)

class List(View):
    def get(self, request):
        uf = AuthCodeForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            codeDb = AuthCode.objects.filter(code = code).first()
            if codeDb:
                codeDb.times += 1
                codeDb.save()
                data = {"status" : 'success',
                        'msg' : '',
                        'data' : []
                        }
                rst = Resume.objects.filter(display__exact = True).values('userEmail', 'addDate', 'content', 'rank')
                for item in rst:
                    item['addDate'] = item['addDate'].strftime('%Y-%m-%d')
                    data['data'].append(item)
                return JsonResponse(data)
            else:
                return JsonResponse({"status" : 'error',
                        'msg' : 'Auth code is error, contact QQ group(Group id:371145284) admin for more information'
                        })

        else:
            return JsonResponse({"stats" : 'error',
                    "msg" : 'AuthCode is illegal'
                    })