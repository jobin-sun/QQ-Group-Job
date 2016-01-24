from django.contrib import admin

# Register your models here.

from .models import User,Resume,AuthCode

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'times')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','qq')
    search_fields = ('email', 'username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('userEmail','display', 'rank')
    search_fields = ('userEmail','content')

admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)