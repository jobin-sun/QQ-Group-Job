from re import compile
from time import time
from api import config
from hashlib import sha1
from base64 import b64encode, b64decode

userTokenPattern = compile(r'(\d+)-(\d{10})-(\w{40})')  # 依次是 用户id-时间戳-token
adminTokenPattern = compile(r'(\d+)-(\d{10})-(\w{40})')  # 依次是 管理员id-时间戳-token

def get_user_sha1(user, timestamp):
    return sha1((user.random + config.keyToken + str(timestamp)).encode('utf-8')).hexdigest()

class Token:
    def __init__(self, timestamp, token_sha1):
        self.timestamp = timestamp
        self.token_sha1 = token_sha1
        self.expired_time = timestamp + config.expiration
    def is_expired(self):
        return int(time()) > self.expired_time
    def is_user(self, user):
        dbtoken = get_user_sha1(user, self.timestamp)
        if self.token_sha1 == dbtoken:
            return True
        else:
            return False

class UserToken(Token):
    def __init__(self, id, timestamp, token_sha1):
        self.id = id
        super().__init__(timestamp, token_sha1)
    def get_token(self):
        return str(self.id) + "-" + str(self.timestamp) + "-" + self.token_sha1

class AdminToken(Token):
    def __init__(self, id, timestamp, token_sha1):
        self.id = id
        super().__init__(timestamp, token_sha1)
    def get_token(self):
        return  str(self.id) + "-" + str(self.timestamp) + "-" + self.token_sha1

def new_userToken(user):
    now = int(time())
    user_sha1 = get_user_sha1(user, now)
    return UserToken(user.id, now, user_sha1)

def new_adminToken(admin):
    now = int(time())
    admin_sha1 = get_user_sha1(admin, now)
    return AdminToken(admin.id, now, admin_sha1)

def parse_userToken(token):
    parse_result = userTokenPattern.match(token)
    if not parse_result:
        return None
    id = int(parse_result.group(1))
    timestamp = int(parse_result.group(2))
    user_sha1 = parse_result.group(3)
    return UserToken(id, timestamp, user_sha1)

def parse_adminToken(token):
    parse_result = adminTokenPattern.match(token)
    if not parse_result:
        return None
    id = int(parse_result.group(1))
    timestamp = int(parse_result.group(2))
    admin_sha1 = parse_result.group(3)
    return AdminToken(id, timestamp, admin_sha1)

