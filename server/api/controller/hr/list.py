__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from api.models import AuthCode, Resume, Rank

from django.forms import (Form, IntegerField, CharField)


class AuthCodeForm(Form):
    groupId = CharField(label=u'群ID：', max_length=15)
    code = IntegerField(min_value=100000, max_value=999999)

class List(View):
    def get(self, request):
        uf = AuthCodeForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            groupId = uf.cleaned_data['groupId']
            codeDb = AuthCode.objects.filter(code__exact = code, groupId__exact = groupId).first()
            if codeDb:
                codeDb.times += 1
                codeDb.save()
                data = {"status" : 'success',
                        'msg' : '',
                        'data' : []
                        }
                rst = Resume.objects.filter(groupId__exact = groupId, display__exact = True).values('id', 'userEmail','groupId','username', 'qq', 'addDate', 'content')
                for item in rst:
                    item['addDate'] = item['addDate'].strftime('%Y-%m-%d')
                    rank = Rank.objects.filter(resumeId__exact = item['id'])
                    if rank:
                        item['rank'] = 0
                        for rankItem in rank:
                            item['rank'] += rankItem['rank']
                        item['rank'] /= len(rank)
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
