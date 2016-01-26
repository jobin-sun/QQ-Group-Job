from django.http import HttpResponse
import json

def index(request):
    data = {
        "status" :  'error',
        'msg' :  'Test Form group reg'
    }
    return HttpResponse(json.dumps(data), content_type="application/json")