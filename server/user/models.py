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
    userEmail = models.EmailField()
    addDate = models.DateTimeField(auto_now_add = True)
    content = models.TextField(blank = True, null = True)
    rank = models.IntegerField(default=0)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['-addDate']

class AuthCode(models.Model):
    code = IntegerRangeField(min_value = 100000, max_value = 999999)
    times = models.IntegerField(default=0)

class Group(models.Model):
    '''群主用户表'''
    groupID = models.CharField(max_length=15) #群号
    ownerQQ = models.CharField(max_length=15) #群主QQ
    password = models.CharField(max_length=40)
    authCode = IntegerRangeField(min_value = 100000, max_value = 999999)
