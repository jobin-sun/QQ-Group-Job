#-*- coding:utf-8 -*-
from django.http import HttpResponse
import json
from api.models import Group

#群主管理群管理员
def index(request):
    if request.method == "GET":
        email = base64.b64decode(request.GET['email'])
        token = request.GET['token']
        user = checkLogin(email,token)
        if not user:
            data = {"status" : "error",
                    "msg" : "User not login"
                    }
        else:
            data = {"status" : 'success',
                    'msg' : '',
                    'data' : []
                    }
            glist = Group.objects.filter(adminName__exact = user.qq,
                userType__exact = 1).values('groupID', 'groupName', 'status')
            for item in glist:
                #一个群有多个管理员,Group每条只包含一个管理的话,主键设置成群号不太合理,   
                admins = Group.objects.filter(groupID__exact = item['groupID'], 
                    userType__exact = 0).values('adminName')
                dic_item = item
                dic_item['admins'] = admins
                data['data'].append(dic_item)
    elif request.method == 'PUT':
        #删除或者管理群管理员权限0删除 1修改
        response = json.loads(request.body.decode("utf-8"))
        opt = response['operation']
        email, token = response['email'], response['token']
        user = checkLogin(email, token) #每次检查是否Login的话用Authorization是不是更好?
        if user:
            data = {"status" :  'success',
                    'msg' :  ''
                    }
            #对群表进行操作待添加
        else:
            data = {"status" : 'error',
                    'msg' : 'User not login'
                    }
    return HttpResponse(json.dumps(data), content_type="application/json")