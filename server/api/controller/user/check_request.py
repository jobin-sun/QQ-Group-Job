__author__ = 'jobin'
from datetime import datetime
from json import loads
from api.token import parse_userToken
from api import config
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
            self.jsonForm = loads(request.body.decode("utf-8"))
        if "token" in self.jsonForm:
            token = self.jsonForm["token"]
        else:
            token = request.COOKIES.get('token')
        if not token:
            self.msg = "Token not found"
            return
        user_token = parse_userToken(token)
        if not user_token:
            self.msg = "Format of token is not correct, Check your token(%s)" % token
            return

        if user_token.is_expired():
            self.msg = "Token is expired, Your time is %s" % datetime.fromtimestamp(
                user_token.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return

        user = User.objects.filter(id__exact = user_token.id).first()
        if not user:
            self.msg = "User not found, Check your id(%s)." % user_token.id
            return

        if user_token.is_user(user):
            self.msg = "User(%s) logined" % user_token.id
            self.user = user
        else:
            self.msg = "Token is illegal, Check your token(%s)" % token

