__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from api.models import AuthCode, Resume, Rank
from django.db.models import Avg

from django.forms import (Form, IntegerField, CharField)


class RequestFrom(Form):
    id = IntegerField()
    groupId = CharField(label=u'群ID：', max_length=15)
    code = IntegerField(min_value=100000, max_value=999999)

class Index(View):
    def get(self, request):
        uf = RequestFrom(request.GET)
        if uf.is_valid():
            id = uf.cleaned_data['id']
            code = uf.cleaned_data['code']
            groupId = uf.cleaned_data['groupId']
            codeDb = AuthCode.objects.filter(code__exact = code, groupId__exact = groupId).first()
            if not codeDb:
                return JsonResponse({"stats" : 'error',
                    'msg' : '授权码无效，请联系群主或管理员(群id:%s)索取正确的授权码' % groupId
                    })
            resume = Resume.objects.filter(id__exact = id, status__exact=1, display__exact = True).values('id','jobTitle', 'userEmail','groupId','username', 'qq', 'sex','age','yearsOfWorking','school','education', 'lastDate', 'content').first()
            avgRank = Rank.objects.filter(resumeId__exact= id).aggregate(Avg('rank'))
            if avgRank:
                resume['rank'] = avgRank['rank__avg']
            else:
                resume['rank'] = -1
            return JsonResponse({
                "status":"success",
                "msg":"",
                "data": resume
            })

        else:
            return JsonResponse({"stats" : 'error',
                    "msg" : 'Form error:%s' % uf.errors
                    })
