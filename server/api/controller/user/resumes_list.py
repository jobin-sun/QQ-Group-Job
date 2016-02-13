__author__ = 'jobin'
import hashlib
import time
import base64

from django.http import JsonResponse
from django.views.generic import View
from django.forms import (Form, PasswordInput, CharField, EmailField)

from .check_request import CheckRequest
from api.models import Resume
from api import config

class Index(View):
    def get(self, request):
        check = CheckRequest(request);
        if not check.user:
            return JsonResponse({
                "status": "error",
                "msg": "User not logined"
            })
        data = {"status" :  "success",
                "msg" :  '',
                "data" : []
                }
        resumes = Resume.objects.filter(userEmail = check.user.email)

        for item in resumes:
            resume = {
                "groupId": item.groupId,
                "username": item.username,
                "qq": item.qq,
                'sex': item.sex,
                'age': item.age,
                'yearsOfWorking': item.yearsOfWorking,
                'school': item.school,
                'education': item.education,
                "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                "content": item.content,
                "status": item.status
            }
            data['data'].append(resume)
        return JsonResponse(data)

