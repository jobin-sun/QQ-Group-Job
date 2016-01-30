__author__ = 'jobin'
__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest


class CheckLogin(View):
    def get(self, request):
        check = CheckRequest(request)
        if check.user:
            data = {"status":"success",
                    "msg":"User logined"
                    }
        else:
            data = {"status":"error",
                    "msg":"User not logined"}
        return JsonResponse(data)