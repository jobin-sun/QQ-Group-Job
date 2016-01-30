__author__ = 'jobin'

from django.http import JsonResponse
from django.views.generic import View
from api.models import User, AuthCode



from django.forms import (Form, EmailField, IntegerField )

class GetUserInfoForm(Form):
    email = EmailField(label=u'电子邮件：')
    code = IntegerField(min_value=100000, max_value=999999)

class Profile(View):
    def get(self, request):
        uf = GetUserInfoForm(request.GET)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            email = uf.cleaned_data['email']
            codeDb = AuthCode.objects.filter(code = code).first()
            if codeDb:
                user = User.objects.filter(email__exact = email).values('email', 'qq', 'username').first()
                if user:
                    data = {"status" : 'success',
                            'msg' : '',
                            'data' : {
                                'email' :  user['email'],
                                'username' : user['username'],
                                'qq' : user['qq']
                                }
                            }
                else:
                    data = {"status" : 'error',
                            'msg' : 'User not found'
                            }
            else:
                data = {"status" : 'error',
                        'msg' : 'AuthCode is illegal'
                        }
            return JsonResponse(data)
        else:
            return JsonResponse({"status" : 'error',
                    'msg' : 'Illegal get'
                    })