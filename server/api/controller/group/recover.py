from django.views.generic import View
from django.http import JsonResponse
from django.forms import Form, PasswordInput, CharField
from json import loads
from api.models import GroupAdmin
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
                owner = GroupAdmin.objects.filter(groupId__exact = token.id, userType__exact = 1).first()
                if owner is None:
                    msg = {
                        "status" : "error",
                        "msg" : "group not exsist"
                    }
                else:
                    if token.is_user(owner):
                        password = db_password(uf.cleaned_data['password'])
                        owner.password = password
                        owner.save()
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

