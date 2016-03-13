from django.views.generic import View
from django.http import JsonResponse
from api.models import GroupAdmin
from api.token import parse_token

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
                owner = GroupAdmin.objects.filter(groupId__exact = token.id, userType__exact = 1).first()
                if owner is None:
                    msg = {
                        "status" : "error",
                        "msg" : "group not exsist"
                    }
                else:
                    if owner.status == 1:
                        msg = {
                            "status" : "error",
                            "msg" : "the group owner already activated"
                        }
                    else:
                        if token.is_user(owner):
                            owner.status = 1
                            owner.save()
                            msg = {
                                "status" : "success",
                                "msg" : "activated"
                            }
                        else:
                            msg = {
                                "status" : "error",
                                "msg" : "error token"
                            }
        return JsonResponse(msg)

