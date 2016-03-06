from re import compile
from time import time
from api import config
from hashlib import sha1
from base64 import b64encode, b64decode
from random import sample
from string import digits, ascii_letters


def get_random(user, token_type):
    if token_type == 'login':
        return user.login_random
    if token_type == 'activate':
        return user.activate_random
    if token_type == 'recover':
        return user.recover_random

def get_sha1(user, timestamp, token_type):
    return sha1((get_random(user, token_type) + config.keyToken + str(timestamp)).encode('utf-8')).hexdigest()


class Token:
    def __init__(self, id, timestamp, token_sha1, token_type):
        self.id = id
        self.timestamp = timestamp
        self.token_sha1 = token_sha1
        self.token_type = token_type
        self.expired_time = timestamp + config.expiration[token_type]

    def is_expired(self):
        return int(time()) > self.expired_time

    def is_user(self, user):
        dbtoken = get_sha1(user, self.timestamp, self.token_type)
        if self.token_sha1 == dbtoken:
            return True
        else:
            return False

    def get_token(self):
        return str(self.id) + "-" + str(self.timestamp) + "-" + self.token_sha1


def new_token(user, token_type):
    now = int(time())
    admin_sha1 = get_sha1(user, now, token_type)
    return Token(user.id, now, admin_sha1, token_type)


def parse_token(token, token_type):
    TokenPattern = compile(r'(\d+)-(\d{10})-(\w{40})')  # 依次是 用户id-时间戳-token
    parse_result = TokenPattern.match(token)
    if not parse_result:
        return None
    id = int(parse_result.group(1))
    timestamp = int(parse_result.group(2))
    user_sha1 = parse_result.group(3)
    return Token(id, timestamp, user_sha1, token_type)

def db_password(password):
    pwd = (password + config.keyPwd).encode('utf-8')
    return sha1(pwd).hexdigest()

def new_random():
    return ''.join(sample(ascii_letters + digits, 10))
