#-*- coding:utf-8 -*-
from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=40)
    username = models.CharField(max_length=50)
    qq = models.CharField(max_length=15)
    random = models.CharField(max_length=10)
    addDate = models.DateTimeField(auto_now_add = True)


class Resume(models.Model):
    statusChoices = (
        (0,u'申请中'),
        (1,u'允许的'),
        (2,u'拒绝的'),
        (3,u'拉黑的'),
    )
    userEmail = models.EmailField(max_length=15)
    groupID = models.CharField(max_length=15) #所属群
    qq = models.CharField(max_length=15)
    lastDate = models.DateTimeField(auto_now = True)
    content = models.TextField(blank = True, null = True)
    display = models.BooleanField(default=True)
    status = models.IntegerField(choices=statusChoices, default=0) # 简历在群中的状态,0:申请中, 1:允许的, 2:拒绝的, 3:拉黑的

    class Meta:
        ordering = ['-lastDate']

class Rank(models.Model):
    resumeId = models.IntegerField();
    groupID = models.CharField(max_length=15) #所属群
    adminName = models.CharField(max_length=15) #群主QQ号或管理员用户名
    rank = models.IntegerField(default=0)
    comment = models.TextField(blank = True, null = True) #管理员评价, 下期做

class AuthCode(models.Model):
    groupID = models.CharField(max_length=15) #所属群
    adminName = models.CharField(max_length=15) #创建者用户名,或群主QQ号
    code = IntegerRangeField(min_value = 100000, max_value = 999999)
    times = models.IntegerField(default=0)
    lastDate = models.DateTimeField(auto_now = True)

    @classmethod
    def create():
        return

    @classmethod
    def create(cls, groupID, adminName, code, times, lastDate):
        code = cls(groupID = groupID, adminName = adminName,
                    code = code, times = times, lastDate = lastDate)
        return code
    

class Group(models.Model):
    '''群列表'''
    statusChoices = (
        (0,u'未验证'),
        (1,u'验证通过'),
        (2,u'验证不通过'),
    )
    groupID = models.CharField(max_length=15,unique=True) #群号
    groupName = models.CharField(max_length=30) #群名称
    addDate = models.DateTimeField(auto_now_add = True)
    requestMsg = models.CharField(max_length=50) # 审核群入驻时,需要加入到群里验证
    status = models.IntegerField(choices=statusChoices, default=0) # 群入驻状态,0:未验证, 1:验证通过, 2:验证不通过
    
class GroupAdmin(models.Model):
    #群管理员列表
    typeChoices = (
         (0, u'管理员'),
         (1, u'群主')
    )
    groupID = models.CharField(max_length=15) #群号
    adminName = models.CharField(max_length=15) #群主QQ号或管理员用户名
    password = models.CharField(max_length=40)
    random = models.CharField(max_length=10)
    userType = models.IntegerField(choices=typeChoices, default=0) # 0:普通管理员, 1:群主

    @classmethod
    def create():
        return

    @classmethod
    def create(cls, groupID, adminName, password, random, userType):
        admin = cls(groupID = groupID, adminName = adminName,
                    password = password, random = random, userType = userType)
        return admin
