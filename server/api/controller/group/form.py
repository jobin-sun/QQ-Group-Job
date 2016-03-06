#-*- coding:utf-8 -*-
from django.forms import (Form, CharField, PasswordInput, IntegerField, ChoiceField)


class PwdForm(Form):
    password = CharField(label=u'密码：', widget=PasswordInput())

class MngResumeForm(Form):
    STATUS_CHOICES = (
        (0,u'申请中'),
        (1,u'允许的'),
        (2,u'拒绝的'),
        (3,u'拉黑的'),
    )
    resumeId = IntegerField()
    status = ChoiceField(choices=STATUS_CHOICES, required=False)
    rank = IntegerField(required=False)

class DelResumeForm(Form):
    resumeId = IntegerField()

class CheckAdminForm(Form):
    admin_qq = CharField(max_length=15)
    password = CharField(widget=PasswordInput())

class DelAdminForm(Form):
    Id = IntegerField()

class AuthCodeForm(Form):
    code = IntegerField(min_value=100000, max_value=999999)

class DelAuthCodeForm(Form):
    Id = IntegerField()
