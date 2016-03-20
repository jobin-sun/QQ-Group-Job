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
    def put(self, request):
        uf = RecoverForm(loads(request.body.decode("utf-8")))
        if not uf.is_valid():
            return JsonResponse({
                "status": "success",
                "msg": "表单提交有误"
            })
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
                admin = GroupAdmin.objects.filter(id__exact = token.id).first()
                if admin is None:
                    msg = {
                        "status" : "error",
                        "msg" : "group not exsist"
                    }
                else:
                    if token.is_user(admin):
                        password = db_password(uf.cleaned_data['password'])
                        admin.password = password
                        admin.save()
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

