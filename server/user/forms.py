from django.core.validators import RegexValidator
from django.forms import (Form, PasswordInput, Textarea,
        CharField, EmailField, BooleanField, IntegerField)

class UserForm(Form):
    username = CharField(label='用户名：', max_length=50)
    password = CharField(label='密码：', widget=PasswordInput())
    qq = CharField(label='QQ：', max_length=15)
    email = EmailField(label='电子邮件：')

class UpdateUserForm(Form):
    email = EmailField(label='电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])
    username = CharField(label='用户名：', max_length=50)
    qq = CharField(label='QQ：', max_length=15)
    display = BooleanField(required=False,initial=False)
    content = CharField(label='详情',required=False,widget=Textarea)

class LoginForm(Form):
    password = CharField(label='密码：', widget=PasswordInput())
    email = EmailField(label='电子邮件：')

class PwdForm(Form):
    email = EmailField(label='电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])
    password = CharField(label='密码：', widget=PasswordInput())
#首页Get请求表单验证
class IndexGetForm(Form):
    email = EmailField(label='电子邮件：')
    token = CharField(label='Token: ', validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
        )
    ])

class AuthCodeForm(Form):
    code = IntegerField(min_value=100000, max_value=999999)

class GetUserInfoForm(Form):
    email = EmailField(label='电子邮件：')
    code = IntegerField(min_value=100000, max_value=999999)

