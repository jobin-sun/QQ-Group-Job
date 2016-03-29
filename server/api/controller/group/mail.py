from django.http import JsonResponse
from django.views.generic import View
from api.send_mail import start_mail_thread
from api.models import GroupAdmin, Group
from api.token import new_token
from api.config import domain, protocol, admin_email, admin_group
from QQJob.settings import BASE_DIR
from django.forms import (Form, CharField)

class ActivaterForm(Form):
    groupId = CharField(max_length=15)
    qq = CharField(max_length=15)
class RecoverForm(Form):
    groupId = CharField(max_length=15)
    qq = CharField(max_length=15)

class Activate(View):
    def get(self, request):
        uf = ActivaterForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "error",
                "msg": "激活邮件发送失败,表单有误"
            })

        groupId = uf.cleaned_data['groupId']
        qq = uf.cleaned_data['qq']
        admin = GroupAdmin.objects.filter(groupId__exact = groupId, qq__exact=qq).first()
        if admin is None:
            msg = {
                "status" : 'error',
                "msg" : 'Admin not exist'
            }
        else:
            if admin.status == 1:
                msg = {
                    "status" : 'error',
                    "msg" : 'group owner already activated'
                }
            else:
                group = Group.objects.filter(groupId__exact=groupId).first()
                if not group:
                    return JsonResponse({
                        "status" : 'error',
                        "msg" : '群ID不存在'
                    })
                with open(BASE_DIR + "/api/mail_template/admin_activate.html", 'rt', encoding='utf-8') as mail_template:
                    template = mail_template.read()
                token = new_token(admin, 'activate')
                token = token.get_token()
                link = "%s://%s/api/group/activate/?token=%s" %(protocol, domain, token)
                email_content = template % (group.groupName, admin.qq, link, admin_email, admin_group)


                start_mail_thread(
                    'Qjob管理员账户激活',
                    email_content,
                    ['%s@qq.com' % admin.qq]
                )

                msg = {
                    "status" : 'success',
                    "msg" : 'email is delivered'
                }
        return JsonResponse(msg)

class Recover(View):
    def get(self, request):
        uf = RecoverForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "error",
                "msg": "邮件发送失败"
            })

        groupId = uf.cleaned_data["groupId"]
        qq = uf.cleaned_data["qq"]
        admin = GroupAdmin.objects.filter(groupId__exact=groupId, qq__exact=qq).first()
        if admin is None:
            msg = {
                "status" : 'error',
                "msg" : '群ID或管理员QQ不存在'
            }
        else:
            group = Group.objects.filter(groupId__exact=groupId).first()
            if not group:
                return JsonResponse({
                    "status" : 'error',
                    "msg" : '群ID不存在'
                })
            with open(BASE_DIR + "/api/mail_template/admin_recover.html", 'rt', encoding='utf-8') as mail_template:
                template = mail_template.read()
            token = new_token(admin, 'recover')
            token = token.get_token()
            link = "%s://%s/#/group/new_pwd/%s" %(protocol, domain, token)
            email_content = template % (group.groupName, admin.qq, link, admin_email, admin_group)

            start_mail_thread(
                'Qjob管理员账户密码重置',
                email_content,
                ['%s@qq.com' % admin.qq]
            )

            msg = {
                "status" : 'success',
                "msg" : 'email is delivered'
            }
        return JsonResponse(msg)

