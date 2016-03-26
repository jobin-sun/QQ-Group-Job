from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from api.response_code import errorCode
from api.models import Group

class Index(View):
    def get(self, request):
        check = CheckRequest(request)
        if not check.admin:
            return JsonResponse({"status": "error",
                                 "code":20000,
                                 "msg": errorCode[20000]})
        checkGroup = Group.objects.filter(groupId__exact = check.admin.groupId).first()
        if checkGroup:
            return JsonResponse({
                "status": "success",
                "msg":"",
                "data":{
                    "groupId": checkGroup.groupId,
                    "groupName": checkGroup.groupName,
                    "status": checkGroup.status,
                }
            })
        else:
            return JsonResponse({"status" : "success",
                                "msg": ""})