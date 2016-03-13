from django.http import JsonResponse
from django.views.generic import View
from api.send_mail import start_mail_thread
from api.models import GroupAdmin
from api.token import new_token
from api.config import email_address
from QQJob.settings import BASE_DIR

class Activate(View):
    def get(self, request):
        groupId = request.GET['id']
        owner = GroupAdmin.objects.filter(groupId__exact = groupId, userType__exact = 1).first()
        if owner is None:
            msg = {
                "status" : 'error',
                "msg" : 'group not exist'
            }
        else:
            if owner.status == 1:
                msg = {
                    "status" : 'error',
                    "msg" : 'group owner already activated'
                }
            else:
                with open(BASE_DIR + "/api/mail_template/activate.html", 'rt') as mail_template:
                    template = mail_template.read()
                token = new_token(owner, 'activate')
                token.id = groupId
                token = token.get_token()
                link = "http://www.qjob.social/api/group/activate/?token=" + token
                email_content = template % ('owner', owner.qq, link)


                start_mail_thread(
                    'Qjob account activate',
                    email_content,
                    email_address,
                    ['%s@qq.com' % owner.qq]
                )

                msg = {
                    "status" : 'success',
                    "msg" : 'email is delivered'
                }
        return JsonResponse(msg)

class Recover(View):
    def get(self, request):
        groupId = request.GET['id']
        owner = GroupAdmin.objects.filter(groupId__exact= groupId, userType__exact = 1).first()
        if owner is None:
            msg = {
                "status" : 'error',
                "msg" : 'group not exist'
            }
        else:
            with open(BASE_DIR + "/api/mail_template/recover.html", 'rt') as mail_template:
                template = mail_template.read()
            token = new_token(owner, 'recover')
            token.id = groupId
            token = token.get_token()
            link = "http://www.qjob.social/api/group/recover/?token=" + token
            email_content = template % ('owner', owner.qq, link)

            start_mail_thread(
                'Qjob account recover',
                email_content,
                email_address,
                ['%s@qq.com' % owner.qq]
            )

            msg = {
                "status" : 'success',
                "msg" : 'email is delivered'
            }
        return JsonResponse(msg)

