__author__ = 'jobin'


from django.http import JsonResponse
from django.views.generic import View

from .check_request import CheckRequest
from api.models import Resume, Group

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
        resumes = Resume.objects.filter(qq__exact = check.user.qq)

        groupIds = []
        for item in resumes:
            groupIds.append(item.groupId)
            resume = {
                "id": item.id,
                "jobTitle": item.jobTitle,
                "email": item.userEmail,
                "groupId": item.groupId,
                "display": item.display,
                "username": item.username,
                "qq": item.qq,
                'sex': item.sex,
                'age': item.age,
                'yearsOfWorking': item.yearsOfWorking,
                'school': item.school,
                'education': item.education,
                "lastDate": item.lastDate,
                #"content": item.content,
                "status": item.status
            }
            data['data'].append(resume)
        groups = Group.objects.filter(groupId__in=groupIds).values("groupId","groupName")
        data["id2name"] = [item for item in groups]
        return JsonResponse(data)

