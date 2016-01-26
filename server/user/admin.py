from django.contrib import admin

# Register your models here.

from .models import User
from .models import Resume
from .models import AuthCode

admin.site.register(User)
admin.site.register(Resume)
admin.site.register(AuthCode)