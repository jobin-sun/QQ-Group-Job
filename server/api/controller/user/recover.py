from django.views.generic import View
from django.http import JsonResponse
from api.models import User
from api.token import parse_token

class Recover(View):
    def get(self, request):
        token_str = request.GET['token']
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

