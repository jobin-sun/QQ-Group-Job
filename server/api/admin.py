from django.contrib import admin

# Register your models here.

from .models import User, Resume, AuthCode, Group, GroupAdmin

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('groupId','adminName', 'code', 'times')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','qq')
    search_fields = ('email', 'username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('userEmail','groupId','qq','display')
    search_fields = ('userEmail','groupId','qq','content')

class GroupList(admin.ModelAdmin):
    list_display = ('groupName','groupId','requestMsg', 'status')
    search_fields = ('groupName','groupId', 'requestMsg')

class GroupAdminAdmin(admin.ModelAdmin):
    list_display = ('groupId', 'password', 'userType')


admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupList)
admin.site.register(GroupAdmin, GroupAdminAdmin)
