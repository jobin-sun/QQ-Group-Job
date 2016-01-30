#-*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from api.models import Resume

#群管理员查看简历列表
def index(request):
    if request.method == "GET":
        data = {"status" : 'success',
                'msg' : '',
                'data' : []
                }
        rst = Resume.objects.filter(display__exact = True).values('userEmail', 'qq', 'lastDate', 'content')
        for item in rst:
            dic_item = item
            dic_item['lastDate'] = item['lastDate'].strftime('%Y-%m-%d')
            data['data'].append(dic_item)
        print data
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {"status" : 'error',
                'msg' : 'Only GET method'
                }
        return HttpResponse(json.dumps(data), content_type="application/json")