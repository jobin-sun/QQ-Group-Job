from django.http import JsonResponse
from django.views.generic import View
from api.send_mail import start_mail_thread
from api.models import User
from api.token import new_token
from api.config import email_address
from QQJob.settings import BASE_DIR

class Activate(View):
    def get(self, request):
        qq = request.GET['qq']
        user = User.objects.filter(qq__exact = qq).first()
        if user is None:
            msg = {
                "status" : 'error',
                "msg" : 'user not exist'
            }
        else:
            if user.status == 1:
                msg = {
                    "status" : 'error',
                    "msg" : 'user already activated'
                }
            else:
                with open(BASE_DIR + "/api/mail_template/activate.html", 'rt') as mail_template:
                    template = mail_template.read()
                token = new_token(user, 'activate').get_token()
                link = "http://www.qjob.social/api/activate/?token=" + token
                email_content = template % ('user', user.qq, link)


                start_mail_thread(
                    'Qjob account activate',
                    email_content,
                    email_address,
                    ['%s@qq.com' % user.qq]
                )

                msg = {
                    "status" : 'success',
                    "msg" : 'email is delivered'
                }
        return JsonResponse(msg)

class Recover(View):
    def get(self, request):
        qq = request.GET['qq']
        user = User.objects.filter(qq__exact= qq).first()
        if user is None:
            msg = {
                "status" : 'error',
                "msg" : 'user not exist'
            }
        else:
            with open(BASE_DIR + "/api/mail_template/recover.html", 'rt') as mail_template:
                template = mail_template.read()
            token = new_token(user, 'recover').get_token()
            link = "http://www.qjob.social/api/recover/?token=" + token
            email_content = template % ('user', user.qq, link)

            start_mail_thread(
                'Qjob account recover',
                email_content,
                email_address,
                ['%s@qq.com' % user.qq]
            )

            msg = {
                "status" : 'success',
                "msg" : 'email is delivered'
            }
        return JsonResponse(msg)

