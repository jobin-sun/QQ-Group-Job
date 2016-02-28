

"""
输入:
    {
        "groupId":"xxxx",
        "groupName":"xxxx",
        "adminName":"xxxx",
        "password":"xxxx",
        "requestMsg":"xxxx"
    }

保存:
    相关表: modules.Group, modules.GroupAdmin

返回:
    {
        "status":"success",#必需
        "msg":"xxxx",#必需
        ....#可选
    }
"""

from django.http import JsonResponse
from django.views.generic import View

from django.forms import (Form, PasswordInput, CharField, EmailField )

from .check_request import CheckRequest
from api.models import Group, GroupAdmin
from api import config
import string
import random
import hashlib


class JoinForm(Form):
    groupId = CharField(label=u'群ID：', max_length=15)
    groupName = CharField(label=u'群名称：', max_length=30)
    adminName = CharField(label=u'群主QQ：', max_length=15)
    password = CharField(label=u'密码：', widget=PasswordInput(), max_length=40)
    requestMsg = CharField(label=u'加群验证信息：', max_length=50)

class Index(View):
    def post(self, request):
        check = CheckRequest(request);
        if check.admin:
            return JsonResponse({
                "status": "error",
                "msg": "User logined"
            })
        uf = JoinForm(check.jsonForm)
        if uf.is_valid():
            #检测群是否存在
            checkGroup = Group.objects.filter(groupId__exact = uf.cleaned_data['groupId']).first()
            if checkGroup:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "此群已在,群ID:%s" % uf.cleaned_data['groupId']
                })
            group = Group()
            group.groupId = uf.cleaned_data['groupId']
            group.groupName = uf.cleaned_data['groupName']
            group.requestMsg = uf.cleaned_data['requestMsg']
            group.save()
            if not group.id:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "Save group error, GroupID:%s" % uf.cleaned_data['groupId']
                })

            admin = GroupAdmin()
            admin.groupId = uf.cleaned_data['groupId']
            admin.adminName = uf.cleaned_data['adminName']
            pwd = (uf.cleaned_data['password'] + config.keyPwd).encode("utf-8")
            admin.password = hashlib.sha1(pwd).hexdigest()
            admin.random = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            admin.userType = 1
            admin.save()
            if admin.id:
                return JsonResponse({
                    "status" : 'success',
                    'msg' : ""
                    })
            else:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "Save group admin error, GroupID:%s; Admin:%s" % (uf.cleaned_data['groupId'], uf.cleaned_data['adminName'])
                    })

        else:
            return JsonResponse({
                "status" : 'error',
                'msg' : "Illegal post: %s" % uf.errors
            })
