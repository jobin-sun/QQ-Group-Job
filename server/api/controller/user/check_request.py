__author__ = 'jobin'
import re
import hashlib
import time
import datetime
import json
from api import config
from base64 import b64decode
from api.models import User

#解析请求中参数,检查用户登录
class CheckRequest():
    def __init__(self, request):
        self.msg = "" #用户状态或,错误信息
        self.jsonForm = {} # 解析GET或POST等方法中参数
        self.user = None
        if request.method == "GET":
            self.jsonForm = request.GET.dict()
        else:
            self.jsonForm = json.loads(request.body.decode("utf-8"))
        if "token" in self.jsonForm:
            token = self.jsonForm["token"]
        else:
            token = request.COOKIES.get('token')
        if not token:
            self.msg = "Token not found"
            return
        pattern = re.compile(r'([\w+=/]+)-(\d{10})-(\w{40})')
        match = pattern.match(token)
        if not match:
            self.msg = "Format of token is not correct, Check your token(%s)" % token
            return
        email = b64decode(match.group(1))
        t = int(match.group(2))
        sha1 = match.group(3)
        now = int(time.time())

        if now - t > config.expiration:
            self.msg = "Token is expired, Your time is %s" % datetime.datetime.fromtimestamp(
                t
            ).strftime('%Y-%m-%d %H:%M:%S')

            return

        user = User.objects.filter(email__exact = email).first()
        if not user:
            self.msg = "User not found, Check your email(%s)." % email
            return

        dbToken = hashlib.sha1(
            (
                user.random + config.keyToken + str(t)
            ).encode("utf-8")
        ).hexdigest()
        if sha1 == dbToken:
            self.msg = "User(%s) logined" % email
            self.user = user
        else:
            self.msg = "Token is illegal, Check your token(%s)" % token

