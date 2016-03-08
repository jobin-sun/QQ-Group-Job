__author__ = 'jobin'


from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from api.models import Resume

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
        resumes = Resume.objects.filter(qq = check.user.qq)

        for item in resumes:
            resume = {
                "id": item.id,
                "email": item.userEmail,
                "groupId": item.groupId,
                "username": item.username,
                "qq": item.qq,
                'sex': item.sex,
                'age': item.age,
                'yearsOfWorking': item.yearsOfWorking,
                'school': item.school,
                'education': item.education,
                "lastDate": item.lastDate.strftime('%Y-%m-%d'),
                #"content": item.content,
                "status": item.status
            }
            data['data'].append(resume)
        return JsonResponse(data)

