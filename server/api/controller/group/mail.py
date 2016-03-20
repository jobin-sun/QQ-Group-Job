from django.http import JsonResponse
from django.views.generic import View
from api.send_mail import start_mail_thread
from api.models import GroupAdmin
from api.token import new_token
from api.config import email_address
from QQJob.settings import BASE_DIR
from api import config
from django.forms import (Form, IntegerField, CharField)

class idForm(Form):
    id = IntegerField()

class recoverForm(Form):
    groupId = CharField(max_length=15)
    qq = CharField(max_length=15)

class Activate(View):
    def get(self, request):
        uf = idForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "success",
                "msg": "激活邮件发送失败"
            })

        id = uf.cleaned_data["id"]
        admin = GroupAdmin.objects.filter(id__exact = id).first()
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
                with open(BASE_DIR + "/api/mail_template/activate.html", 'rt') as mail_template:
                    template = mail_template.read()
                token = new_token(admin, 'activate')
                token = token.get_token()
                link = "%s://%s/api/group/activate/?token=%s" %(config.protocol, config.domain, token)
                email_content = template % ('owner', admin.qq, link)


                start_mail_thread(
                    'Qjob account activate',
                    email_content,
                    email_address,
                    ['%s@qq.com' % admin.qq]
                )

                msg = {
                    "status" : 'success',
                    "msg" : 'email is delivered'
                }
        return JsonResponse(msg)

class Recover(View):
    def get(self, request):
        uf = recoverForm(request.GET)
        if not uf.is_valid():
            return JsonResponse({
                "status": "success",
                "msg": "邮件发送失败"
            })

        groupId = uf.cleaned_data["groupId"]
        qq = uf.cleaned_data["qq"]
        admin = GroupAdmin.objects.filter(groupId__exact=groupId, qq__exact=qq).first()
        if admin is None:
            msg = {
                "status" : 'error',
                "msg" : 'group not exist'
            }
        else:
            with open(BASE_DIR + "/api/mail_template/recover.html", 'rt') as mail_template:
                template = mail_template.read()
            token = new_token(admin, 'recover')
            token = token.get_token()
            link = "%s://%s/#/group/new_pwd/%s" %(config.protocol, config.domain, token)
            email_content = template % ('owner', admin.qq, link)

            start_mail_thread(
                'Qjob account recover',
                email_content,
                email_address,
                ['%s@qq.com' % admin.qq]
            )

            msg = {
                "status" : 'success',
                "msg" : 'email is delivered'
            }
        return JsonResponse(msg)

