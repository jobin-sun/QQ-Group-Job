from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect
from api.models import GroupAdmin
from api.token import parse_token
from api.token import new_token

class Activate(View):
    def get(self, request):
        token_str = request.GET['token']
        token = parse_token(token_str, 'activate')

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
                    if admin.status == 1:
                        msg = {
                            "status" : "error",
                            "msg" : "The admin already activated"
                        }
                    else:
                        if token.is_user(admin):
                            admin.status = 1
                            admin.save()
                            if admin.userType == 0:
                                token = new_token(admin, 'recover')
                                token.id = admin.id
                                token = token.get_token()
                                return HttpResponseRedirect('/#/group/new_pwd/'+token)
                            else:
                                return HttpResponseRedirect('/#/group/login')
                        else:
                            msg = {
                                "status" : "error",
                                "msg" : "error token"
                            }
        return JsonResponse(msg)

