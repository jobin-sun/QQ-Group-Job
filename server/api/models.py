#-*- coding:utf-8 -*-
from django.db import models


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
# Create your models here.


class User(models.Model):
    sexChoices = (
        (0, u'保密'),
        (1, u'男'),
        (2, u'女')
    )
    eduChoices = (
        (0, u'大专以下'),
        (1, u'大专'),
        (2, u'本科'),
        (3, u'硕士'),
        (4, u'硕士以上')
    )
    activate = (
        (0, u'未激活'),
        (1, u'已激活')
    )
    password = models.CharField(max_length=40)
    username = models.CharField(max_length=50)
    qq = models.CharField(max_length=15, unique=True)

    status = models.IntegerField(default=0, choices=activate)

    sex = models.IntegerField(default=0, choices=sexChoices)
    age = IntegerRangeField(default=20, min_value=15, max_value=100)
    yearsOfWorking = IntegerRangeField(default=0, min_value=0, max_value=60)
    school = models.CharField(max_length=40)
    education = models.IntegerField(default=2, choices=eduChoices)

    activate_random = models.CharField(max_length=10)
    recover_random = models.CharField(max_length=10)
    login_random = models.CharField(max_length=10)

    addDate = models.DateTimeField(auto_now_add=True)


class Resume(models.Model):
    statusChoices = (
        (0, u'申请中'),
        (1, u'允许的'),
        (2, u'拒绝的'),
        (3, u'拉黑的'),
    )
    sexChoices = (
        (0, u'保密'),
        (1, u'男'),
        (2, u'女')
    )
    eduChoices = (
        (0, u'大专以下'),
        (1, u'大专'),
        (2, u'本科'),
        (3, u'硕士'),
        (4, u'硕士以上')
    )
    groupId = models.CharField(max_length=15)  # 所属群
    qq = models.CharField(max_length=15)

    userEmail = models.EmailField(max_length=15)
    username = models.CharField(max_length=50)
    sex = models.IntegerField(default=0, choices=sexChoices)
    age = IntegerRangeField(default=20, min_value=15, max_value=100)
    yearsOfWorking = IntegerRangeField(default=0, min_value=0, max_value=60)
    school = models.CharField(max_length=40)
    education = models.IntegerField(default=2, choices=eduChoices)

    lastDate = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, null=True)
    display = models.BooleanField(default=True)
    # 简历在群中的状态,0:申请中, 1:允许的, 2:拒绝的, 3:拉黑的
    status = models.IntegerField(choices=statusChoices, default=0)

    class Meta:
        ordering = ['-lastDate']


class Rank(models.Model):
    resumeId = models.IntegerField()
    admin_qq = models.CharField(max_length=15)  # 群主QQ号或管理员QQ号
    rank = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)  # 管理员评价, 下期做


class AuthCode(models.Model):
    groupId = models.CharField(max_length=15)  # 所属群
    admin_qq = models.CharField(max_length=15)  # 创建者用户名,或群主QQ号
    code = IntegerRangeField(min_value=100000, max_value=999999)
    times = models.IntegerField(default=0)
    lastDate = models.DateTimeField(auto_now=True)


class Group(models.Model):
    '''群列表'''
    statusChoices = (
        (0, u'未验证'),
        (1, u'验证通过'),
        (2, u'验证不通过'),
    )
    groupId = models.CharField(max_length=15, unique=True)  # 群号
    groupName = models.CharField(max_length=30)  # 群名称
    addDate = models.DateTimeField(auto_now_add=True)
    # 群入驻状态,0:未验证, 1:验证通过, 2:验证不通过
    status = models.IntegerField(choices=statusChoices, default=0)

    def delete(self):
        admins = GroupAdmin.objects.filter(groupId__exact=self.groupId)
        for admin in admins:
            admin.delete()
        super(Group, self).delete()

class GroupAdmin(models.Model):
    # 群管理员列表
    typeChoices = (
        (0, u'管理员'),
        (1, u'群主')
    )
    activate = (
        (0, u'未激活'),
        (1, u'已激活')
    )
    groupId = models.CharField(max_length=15)  # 群号
    admin_qq = models.CharField(max_length=15)

    login_random = models.CharField(max_length=10)
    activate_random = models.CharField(max_length=10)
    recover_random = models.CharField(max_length=10)

    password = models.CharField(max_length=40)
    status = models.IntegerField(choices=activate, default=0)
    userType = models.IntegerField(choices=typeChoices, default=0) # 0:普通管理员, 1:群主

