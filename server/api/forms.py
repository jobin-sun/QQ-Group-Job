#-*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.forms import (Form, PasswordInput, Textarea,
        CharField, EmailField, BooleanField, IntegerField)

class UserForm(Form):
    username = CharField(label=u'用户名：', max_length=50)
    password = CharField(label=u'密码：', widget=PasswordInput())
    qq = CharField(label='QQ：', max_length=15)
    email = EmailField(label=u'电子邮件：')

class UpdateUserForm(Form):
    email = EmailField(label=u'电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])
    username = CharField(label=u'用户名：', max_length=50)
    qq = CharField(label='QQ：', max_length=15)
    display = BooleanField(required=False,initial=False)
    content = CharField(label=u'详情',required=False,widget=Textarea)

class LoginForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())
    email = EmailField(label=u'电子邮件：')

class PwdForm(Form):
    email = EmailField(label=u'电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])
    password = CharField(label=u'密码：', widget=PasswordInput())
#首页Get请求表单验证
class IndexGetForm(Form):
    email = EmailField(label=u'电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])

class AuthCodeForm(Form):
    code = IntegerField(min_value=100000, max_value=999999)

class GetUserInfoForm(Form):
    email = EmailField(label=u'电子邮件：')
    code = IntegerField(min_value=100000, max_value=999999)

class GroupForm(Form):
    groupID = CharField(label=u'群ID：', max_length=15)
    ownerQQ = CharField(label=u'群主QQ：', max_length=15)
    password = CharField(label=u'密码：', widget=PasswordInput())
    authCode = IntegerField(min_value=100000, max_value=999999)
        