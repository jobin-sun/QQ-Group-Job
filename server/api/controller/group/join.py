

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
from api.token import db_password, new_random


class JoinForm(Form):
    groupId = CharField(label=u'群ID：', max_length=15)
    groupName = CharField(label=u'群名称：', max_length=30)
    ownerqq = CharField(label=u'群主QQ：', max_length=15)
    password = CharField(label=u'密码：', widget=PasswordInput(), max_length=40)

class Index(View):
    def post(self, request):
        check = CheckRequest(request);
        if check.admin:
            return JsonResponse({
                "status": "error",
                "msg": "User logined"
            })
        uf = JoinForm(check.jsonForm)
        groupId = uf.cleaned_data['groupId']
        groupName = uf.cleaned_data['groupName']
        ownerqq = uf.cleaned_data['ownerqq']
        password = uf.cleaned_data['password']
        if uf.is_valid():
            #检测群是否存在
            checkGroup = Group.objects.filter(groupId__exact = groupId).first()
            if checkGroup:
                if checkGroup.state == 0:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "此群已被注册,但正在验证中,群ID:%s" % groupId
                    })
                if checkGroup.state == 1:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "此群已被注册并验证通过,可申请转让,群ID:%s" % groupId
                    })
                if checkGroup.state == 2:
                    GroupAdmin.objects.filter(groupId__exact = groupId).delete()
                    checkGroup.delete()
                group = Group(
                    groupId = groupId,
                    groupName = groupName
                )
                group.save()
                if not group.id:
                    return JsonResponse({
                        "status" : 'error',
                        'msg' : "Save group error, GroupID:%s" % uf.cleaned_data['groupId']
                    })

                admin = GroupAdmin(
                    groupId = groupId,
                    qq = ownerqq,
                    password = db_password(password),
                    login_random = new_random(),
                    activate_random = new_random(),
                    recover_random = new_random(),
                    userType = 1
                    )
                admin.save()
                if admin.id:
                    return JsonResponse({
                        "status" : 'success',
                        'msg' : ""
                    })
            else:
                return JsonResponse({
                    "status" : 'error',
                    'msg' : "Save group admin error, GroupID:%s; Admin:%s" % (groupId, ownerqq)
                    })

        else:
            return JsonResponse({
                "status" : 'error',
                'msg' : "Illegal post: %s" % uf.errors
            })
