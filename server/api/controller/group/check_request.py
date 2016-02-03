__author__ = 'jobin'
import re
import hashlib
import time
import datetime
import json
from api import config
from api.models import GroupAdmin

#解析请求中参数,检查用户登录
'''
传入request对象
不管哪种方法,请求参数将被放到self.jsonForm里
管理员token信息保存在admin_token里,格式及方法基本与普通用户的相同,格式见下面代码里的pattern正则
self.admin保存里权限验证通过的admin信息, 如果self.admin为None,则是没有登录的用户,

'''
class CheckRequest():
    def __init__(self, request):
        self.msg = "" #用户状态或,错误信息
        self.jsonForm = {} # 解析GET或POST等方法中参数
        self.admin = None
        if request.method == "GET":
            self.jsonForm = request.GET.dict()
        else:
            self.jsonForm = json.loads(request.body.decode("utf-8"))
        if "admin_token" in self.jsonForm:
            token = self.jsonForm["admin_token"]
        else:
            token = request.COOKIES.get('admin_token')
        if not token:
            self.msg = "Token not found"
            return
        pattern = re.compile(r'(\d+)-(\w+)-(\d{10})-(\w{40})')#依次是群id-管理员用户名-时间戳-token
        match = pattern.match(token)
        if not match:
            self.msg = "Format of token is not correct, Check your token(%s)" % token
            return
        groupID = match.group(1)
        adminName = match.group(2)
        t = int(match.group(3))
        sha1 = match.group(4)
        now = int(time.time())

        if now - t > config.expiration:
            self.msg = "Token is expired, Your time is %s" % datetime.datetime.fromtimestamp(
                t
            ).strftime('%Y-%m-%d %H:%M:%S')

            return

        admin = GroupAdmin.objects.filter(groupID__exact = groupID, adminName__exact = adminName).first()
        if not admin:
            self.msg = "Admin not found, groupId:%s; adminName." % groupID, adminName
            return

        dbToken = hashlib.sha1(
            (
                admin.random + config.keyToken + str(t)
            ).encode("utf-8")
        ).hexdigest()
        if sha1 == dbToken:
            self.msg = "Admin logined"
            self.admin = admin
        else:
            self.msg = "Token is illegal, Check your token(%s)" % token

