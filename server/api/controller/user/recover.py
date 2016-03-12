from django.views.generic import View
from django.http import JsonResponse
from django.forms import Form, PasswordInput, CharField
from json import loads
from api.models import User
from api.token import parse_token, db_password


class RecoverForm(Form):
    token = CharField(label=u'token: ')
    password = CharField(label=u'密码: ', widget=PasswordInput())


class Recover(View):
    def post(self, request):
        uf = RecoverForm(loads(request.body.decode("utf-8")))
        token_str = uf.cleaned_data['token']
        token = parse_token(token_str, 'recover')
        if token is None:
            msg = {
                "status" : "error",
                "msg" : "error token"
            }
        else:
            if token.is_expired():
                msg = {
                    "status" : "error",
                    "msg" : "token is expired"
                }
            else:
                user = User.objects.filter(id__exact = token.id).first()
                if user is None:
                    msg = {
                        "status" : "error",
                        "msg" : "user not exsist"
                    }
                else:
                    if token.is_user(user):
                        password = db_password(uf.cleaned_data['password'])
                        user.password = password
                        user.save()
                        msg = {
                            "status" : "success",
                            "msg" : "authentication is successful"
                        }
                    else:
                        msg = {
                            "status" : "error",
                            "msg" : "error token"
                        }
        return JsonResponse(msg)

