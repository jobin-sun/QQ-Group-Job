#-*- coding:utf-8 -*-

import json
from user.models import User, Resume, AuthCode
from user.forms import (
        UserForm, UpdateUserForm, LoginForm,
        PwdForm, IndexGetForm, AuthCodeForm,
        GetUserInfoForm)
from django.http import HttpResponse
from django.core.validators import RegexValidator
import base64
import random
import string
import hashlib
import time

keyPwd = "aad3338()(*23ddDGKLhhdaf@3fasdfd-ddd"
keyToken = "defkjhsddfnnd#$%didfnDs"

def checkLogin(email, token):
    #检测用户登录
    uf = IndexGetForm({
        "email":email,
        "token":token
    })
    if uf.is_valid():
        email = uf.cleaned_data['email']
        token = uf.cleaned_data['token']
        user = User.objects.filter(email__exact = email).first()
    else:
        return False
    if not user:
        return  False
    dbToken = hashlib.sha1(
            (
                user.random + keyToken + str(int(time.time() / (24 * 3600)))
                ).encode("utf-8")
            ).hexdigest()
    if token != dbToken:
        return False
    return user


#用户首页
def index(request):
    if request.method == 'GET':
        email = base64.b64decode(request.GET['email'])
        token = request.GET['token']
        #检测用户登录
        user = checkLogin(email,token)
        if not user:
            data = {"status" : "error",
                    "msg" : "User not login"
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
        data = {"status" :  "success",
                "msg" :  '',
                "data" :  {
                    "email" : user.email,
                    "username" :  user.username,
                    "qq" : user.qq,
                    "addDate" :  user.addDate.strftime('%Y-%m-%d')
                    }
                }
        resume = Resume.objects.filter(userEmail__exact = email).first()
        if resume:
            data['data'].update({
                "content" : resume.content,
                "display" : resume.display,
                "contentDate" : resume.addDate.strftime('%Y-%m-%d %H:%m')
                })
        return HttpResponse(json.dumps(data), content_type="application/json")

    elif request.method == 'PUT':
        rst = json.loads(request.body.decode("utf-8"))
        rst['email'] = base64.b64decode(rst['email'])
        uf = UpdateUserForm(rst)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            token = uf.cleaned_data['token']
            #检测用户登录
            user = checkLogin(email,token)
            if not user:
                data = {"status" : "error",
                        "msg" : "User not login"
                        }
                return HttpResponse(json.dumps(data), content_type="application.json")
            user.username = uf.cleaned_data['username']
            user.qq = uf.cleaned_data['qq']
            user.save()
            resume = Resume.objects.filter(userEmail__exact = email).first()
            if not resume:
                resume = Resume()
                resume.userEmail = email
            resume.content = uf.cleaned_data['content']
            resume.display = uf.cleaned_data['display']
            resume.save()

            data = {"status" : "success",
                    "msg" :  ''
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {"status" : "error",
                    "msg" : 'Form error'
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")

def changePwd(request):
    if request.method == 'PUT':
        rst = json.loads(request.body.decode("utf-8"))
        rst['email'] = base64.b64decode(rst['email'])
        uf = PwdForm(rst)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            token = uf.cleaned_data['token']
            #检测用户登录
            user = checkLogin(email,token)
            if not user:
                data = {"status" : 'error',
                        'msg' : 'User not login'
                        }
                return HttpResponse(json.dumps(data), content_type="application/json")
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            user.password = hashlib.sha1(pwd).hexdigest()
            user.save()
            data = {"status" :  'success',
                    'msg' :  ''
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {"status" :  'error',
                    'msg' :  'Form error'
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")

#HR根据授权码及邮件地址查看用户资料
def getUserInfo(request):
    if request.method == 'GET':
        uf = GetUserInfoForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            email = uf.cleaned_data['email']
            codeDb = AuthCode.objects.filter(code = code).first()
            if codeDb:
                user = User.objects.filter(email__exact = email).values('email', 'qq', 'username').first()
                if user:
                    data = {"status" : 'success',
                            'msg' : '',
                            'data' : {
                                'email' :  user['email'],
                                'username' : user['username'],
                                'qq' : user['qq']
                                }
                            }
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = {"status" : 'error',
                            'msg' : 'User not found'
                            }
            else:
                data = {"status" : 'error',
                        'msg' : 'AuthCode is illegal'
                        }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {"status" : 'error',
                    'msg' : 'Form error'
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {"status" : 'error',
                'msg' : 'Only GET method'
                }
        return HttpResponse(json.dumps(data), content_type="application/json")

#简历页面
def list(request):
    if request.method == "GET":
        uf = AuthCodeForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            codeDb = AuthCode.objects.filter(code = code).first()
            if codeDb:
                codeDb.times += 1
                codeDb.save()
                data = {"status" : 'success',
                        'msg' : '',
                        'data' : []
                        }
                rst = Resume.objects.filter(display__exact = True).values('userEmail', 'addDate', 'content', 'rank')
                for item in rst:
                    item['addDate'] = item['addDate'].strftime('%Y-%m-%d')
                    data['data'].append(item)
                response = HttpResponse(json.dumps(data), content_type="application/json")
                return response
            else:
                data = {"status" : 'error',
                        'msg' : 'Auth code is error, contact QQ group(Group id:371145284) admin for more information'
                        }
                return HttpResponse(json.dumps(data), content_type="application/json")

        else:
            data = {"stats" : 'error',
                    "msg" : 'AuthCode is illegal'
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        data = {"status" : 'error',
                'msg' : "Only get method"
                }
        return HttpResponse(json.dumps(data), content_type="application/json")

#注册
def register(request):
    if request.method == "POST":
        rst = json.loads(request.body.decode("utf-8"))
        uf = UserForm(rst)
        if uf.is_valid():
            #检测用户是否存在
            checkUser = User.objects.filter(email__exact = uf.cleaned_data['email']).first()
            if checkUser:
                data = {"status" : 'error',
                        'msg' : "此Email账户已存在"
                        }
                return HttpResponse(json.dumps(data), content_type="application/json")
            user = User()
            user.username = uf.cleaned_data['username']
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            user.password = hashlib.sha1(pwd).hexdigest()
            user.qq = uf.cleaned_data['qq']
            user.email = uf.cleaned_data['email']
            user.random = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            user.save()

            data = {"status" : 'success',
                    'msg' : ""
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {"status" : 'error',
                    'msg' : "Illegal post"
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {"status" : 'error',
                'msg' : "Only post method"
                }

        return HttpResponse(json.dumps(data), content_type="application/json")

#登录
def login(request):
    if request.method == 'POST':
        rst = json.loads(request.body.decode("utf-8"))
        uf = LoginForm(rst)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            password = hashlib.sha1(pwd).hexdigest()
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(email__exact = email,password__exact = password).first()
            if user:
                data = {"status" : 'success',
                        'msg' : "Login success"
                        }

                #将username写入浏览器cookie,失效时间为3600 * 24 * 30

                token = hashlib.sha1((user.random + keyToken + str(int(time.time() / (24 * 3600)))).encode("utf-8")).hexdigest()
                cookieOpt = {'expires' : int(time.time()) + 3600 * 24 * 30}
                data['cookies'] = {
                        'email' : {
                            'value' : base64.b64encode(email.encode('utf-8')).decode("utf-8"),
                            'opt' : cookieOpt
                            },
                        'token' : {
                            'value' : token,
                            'opt' : cookieOpt
                            }
                        }
                response = HttpResponse(json.dumps(data), content_type="application/json")
                return response
            else:
                #比较失败，还在login
                data = {"status" : 'error',
                        'msg' : "email or password is error"
                        }
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {"status" :'error',
                    'msg' : "login form is error"
                    }
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:

        data = {"status" : 'error',
                'msg' : "login only post method"
                }
        return HttpResponse(json.dumps(data), content_type="application/json")
