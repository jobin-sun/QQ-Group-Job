__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from api.models import AuthCode, Resume, Rank
from django.db.models import Avg

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


                rst = Resume.objects.filter(groupId__exact = groupId, status__exact=1, display__exact = True).order_by("-lastDate").values('id','jobTitle', 'userEmail','groupId','username', 'qq', 'sex','age','yearsOfWorking','school','education', 'lastDate', 'content')
                allRank = Rank.objects.filter(groupId__exact= groupId)
                for item in rst:
                    adminsRank = allRank.filter(resumeId__exact = item["id"])
                    avgRank = adminsRank.aggregate(Avg('rank'))
                    item['rank'] = -1
                    if avgRank:
                        item['rank'] = avgRank['rank__avg']
                    data['data'].append(item)
                return JsonResponse(data)
            else:
                return JsonResponse({"status" : 'error',
                        'msg' : '授权码无效，请联系群主或管理员(群id:%s)索取正确的授权码' % groupId
                        })

        else:
            return JsonResponse({"stats" : 'error',
                    "msg" : 'AuthCode is illegal'
                    })
