from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from .form import CheckAdminForm, DelAdminForm, MngResumeForm
from api.models import GroupAdmin, Resume, User
from api.token import db_password, new_random

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status" : "error",
                                "msg" : "Only admin permitted"})

        return JsonResponse({
            "status": "success",
            "msg":"",
            "data":{
                "groupId": check.admin.groupId,
                "qq": check.admin.qq,
                "nick": check.admin.nick,
                "userType": check.admin.userType
            }
        })
