__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View


class Logout(View):
    def get(self, request):

        response = JsonResponse({"status":"success",
                                 "msg":""
                                 })
        response.delete_cookie("token")
        response.delete_cookie("logined")
        return  response