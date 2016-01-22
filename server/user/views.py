from django.http import HttpResponse
import json
from user.models import User
from user.models import Resume
from user.models import AuthCode
from django import forms
from django.http import QueryDict
from django.http import HttpResponse,HttpResponseRedirect
import base64
import random
import string
import hashlib
import time

keyPwd = "defkjhsddfnnd#$%didfnDs"
keyToken = "defkjhsddfnnd#$%didfnDs"

class UserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=50)
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())
    qq = forms.CharField(label='QQ：', max_length=15)
    email = forms.EmailField(label='电子邮件：')

class UpdateUserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=50)
    qq = forms.CharField(label='QQ：', max_length=15)
    display = forms.BooleanField(required=False,initial=False)
    content = forms.CharField(label='详情',required=False,widget=forms.Textarea)

class LoginForm(forms.Form):
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件：')

class PwdForm(forms.Form):
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())

class AuthCodeForm(forms.Form):
    code = forms.IntegerField(min_value=100000, max_value=999999)

def changePwd(request):
    email = request.COOKIES.get('email','')
    email = base64.b64decode(email)
    token = request.COOKIES.get('token')
    user = User.objects.filter(email__exact = email).first()
    if not user:
        data = {}
        data["status"] = 'error'
        data['msg'] = 'User not found'
        return HttpResponse(json.dumps(data), content_type="application/json")
    dbToken = hashlib.sha1((user.random + keyToken + str(int(time.time() / (24 * 3600)))).encode("utf-8")).hexdigest()
    if token != dbToken:
        data = {}
        data["status"] = 'error'
        data['msg'] = 'Token error'
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == 'PUT':
        rst = json.loads(request.body.decode("utf-8"))
        uf = PwdForm(rst)
        if uf.is_valid():
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            user.password = hashlib.sha1(pwd).hexdigest()
            user.save()
            data = {}
            data["status"] = 'success'
            data['msg'] = ''
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {}
            data["status"] = 'error '
            data['msg'] = 'Form error'
            return HttpResponse(json.dumps(data), content_type="application/json")

def getUserInfo(request):
    if request.method == 'GET':
        code = request.COOKIES.get('auth_code','')
        codeDb = AuthCode.objects.filter(code = code).first()
        if codeDb:
            email = request.GET['email']
            if not email:
                data = {}
                data["status"] = 'error'
                data['msg'] = 'Email can not empty'
            user = User.objects.filter(email__exact = email).values('email', 'qq', 'username').first()
            if user:
                data = {}
                data["status"] = 'success'
                data['msg'] = ''
                data['data'] = {}
                data['data']['email'] = user['email']
                data['data']['username'] = user['username']
                data['data']['qq'] = user['qq']
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = {}
                data["status"] = 'error'
                data['msg'] = 'User not found'
        else:
            data = {}
            data["status"] = 'error'
            data['msg'] = 'AuthCode is illegal'
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {}
        data["status"] = 'error'
        data['msg'] = 'Only GET method'
        return HttpResponse(json.dumps(data), content_type="application/json")

def index(request):
    email = request.COOKIES.get('email','')
    email = base64.b64decode(email)
    token = request.COOKIES.get('token')
    user = User.objects.filter(email__exact = email).first()
    if not user:
        data = {}
        data["status"] = 'error'
        data['msg'] = 'User not found'
        return HttpResponse(json.dumps(data), content_type="application/json")
    dbToken = hashlib.sha1((user.random + keyToken + str(int(time.time() / (24 * 3600)))).encode("utf-8")).hexdigest()
    if token != dbToken:
        data = {}
        data["status"] = 'error'
        data['msg'] = 'Token error'
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == 'PUT':
        rst = json.loads(request.body.decode("utf-8"))
        uf = UpdateUserForm(rst)
        if uf.is_valid():
            user.username = uf.cleaned_data['username']
            user.qq = uf.cleaned_data['qq']
            user.save()
            resume = Resume.objects.filter(userEmail__exact = email).first()
            if resume:
                resume.content = uf.cleaned_data['content']
                resume.display = uf.cleaned_data['display']
                resume.save()
            else:
                resume = Resume()
                resume.userEmail = email
                resume.content = uf.cleaned_data['content']
                resume.display = uf.cleaned_data['display']
                resume.save()
            data = {}
            data["status"] = 'success'
            data['msg'] = ''
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {}
            data["status"] = 'error '
            data['msg'] = 'Form error'
            return HttpResponse(json.dumps(data), content_type="application/json")

    elif request.method == 'GET':
        data = {}
        data["status"] = 'success'
        data['msg'] = ''
        data['data'] = {}
        data['data']['email'] = user.email
        data['data']['username'] = user.username
        data['data']['qq'] = user.qq
        data['data']['addDate'] = user.addDate.strftime('%Y-%m-%d')
        resume = Resume.objects.filter(userEmail__exact = email).first()
        if resume:
            data['data']['content'] = resume.content
            data['data']['display'] = resume.display
            data['data']['contentDate'] = resume.addDate.strftime('%Y-%m-%d %H:%m')
        return HttpResponse(json.dumps(data), content_type="application/json")



def list(request):
    if request.method == "GET":
        uf = AuthCodeForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            codeDb = AuthCode.objects.filter(code = code).first()
            if codeDb:
                codeDb.times += 1
                codeDb.save()
                data = {}
                data["status"] = 'success'
                data['msg'] = ''
                data['data'] = []
                rst = Resume.objects.filter(display__exact = True).values('userEmail', 'addDate', 'content', 'rank')
                for item in rst:
                    item['addDate'] = item['addDate'].strftime('%Y-%m-%d')
                    data['data'].append(item)
                response = HttpResponse(json.dumps(data), content_type="application/json")
                response.set_cookie('auth_code', code, 3600)
                return response
            else:
                data = {}
                data["status"] = 'error'
                data['msg'] = 'Auth code is error, contact QQ group(Group id:371145284) admin for more information'
                return HttpResponse(json.dumps(data), content_type="application/json")

        else:
            data = {}
            data["stats"] = 'error'
            data['msg'] = 'AuthCode is illegal'
            return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        data = {}
        data["status"] = 'error'
        data['msg'] = "Only get method"
        return HttpResponse(json.dumps(data), content_type="application/json")


def register(request):
    if request.method == "POST":
        rst = json.loads(request.body.decode("utf-8"))
        uf = UserForm(rst)
        if uf.is_valid():
            #检测用户是否存在
            checkUser = User.objects.filter(email__exact = uf.cleaned_data['email']).first()
            if checkUser:
                data = {}
                data["status"] = 'error'
                data['msg'] = "此Email账户已存在"
                return HttpResponse(json.dumps(data), content_type="application/json")
            user = User()
            user.username = uf.cleaned_data['username']
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            user.password = hashlib.sha1(pwd).hexdigest()
            user.qq = uf.cleaned_data['qq']
            user.email = uf.cleaned_data['email']
            user.random = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            user.save()

            data = {}
            data["status"] = 'success'
            data['msg'] = ""
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {}
            data["status"] = 'error'
            data['msg'] = "Illegal post"
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {}
        data["status"] = 'error'
        data['msg'] = "Only post method"

        return HttpResponse(json.dumps(data), content_type="application/json")

def login(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email','')
        email = base64.b64decode(email)
        token = request.COOKIES.get('token')
        if email and token:
            user = User.objects.filter(email__exact = email).first()
            if user:
                dbToken = hashlib.sha1((user.random + keyToken + str(int(time.time() / (24 * 3600)))).encode("utf-8")).hexdigest()
                if token == dbToken:
                    data = {}
                    data["status"] = 'success'
                    data['msg'] = 'User logined'
                    return HttpResponse(json.dumps(data), content_type="application/json")

        rst = json.loads(request.body.decode("utf-8"))
        uf = LoginForm(rst)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            pwd = (uf.cleaned_data['password'] + keyPwd).encode("utf-8")
            password = hashlib.sha1(pwd).hexdigest()
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(email__exact = email,password__exact = password).first()
            if user:
                data = {}
                data["status"] = 'success'
                data['msg'] = "Login success"
                response = HttpResponse(json.dumps(data), content_type="application/json")
                #将username写入浏览器cookie,失效时间为3600 * 24 * 30

                token = hashlib.sha1((user.random + keyToken + str(int(time.time() / (24 * 3600)))).encode("utf-8")).hexdigest()
                response.set_cookie('email',base64.b64encode(email.encode('utf-8')),3600 * 24 * 30)
                response.set_cookie('token',token,3600 * 24 * 30)
                return response
            else:
                #比较失败，还在login
                data = {}
                data["status"] = 'error'
                data['msg'] = "email or password is error"
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {}
            data["status"] = 'error'
            data['msg'] = "login form is error"
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:

        data = {}
        data["status"] = 'error'
        data['msg'] = "login only post method"
        return HttpResponse(json.dumps(data), content_type="application/json")