__author__ = 'jobin'
from datetime import datetime
from json import loads
from api.token import parse_token
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
            self.jsonForm = loads(request.body.decode("utf-8"))
        if "admin_token" in self.jsonForm:
            token = self.jsonForm["admin_token"]
        else:
            token = request.COOKIES.get('admin_token')
        if not token:
            self.msg = "Token not found"
            return
        admin_token = parse_token(token, 'login')
        if admin_token is None:
            self.msg = "Format of token is not correct, Check your token(%s)" % token
            return

        if admin_token.is_expired():
            self.msg = "Token is expired, Your time is %s" % datetime.fromtimestamp(
                admin_token.timestamp).strftime('%Y-%m-%d %H:%M:%S')

            return

        admin = GroupAdmin.objects.filter(id__exact = admin_token.id).first()
        if not admin:
            self.msg = "Admin not found, id" % admin_token.id
            return

        if admin_token.is_user(admin):
            self.msg = "Admin logined"
            self.admin = admin
        else:
            self.msg = "Token is illegal, Check your token(%s)" % token

