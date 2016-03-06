from django.contrib import admin

# Register your models here.

from .models import User, Resume, AuthCode, Group, GroupAdmin

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('groupId','admin_qq', 'code', 'times')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','qq')
    search_fields = ('username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('userEmail','groupId','qq','display')
    search_fields = ('userEmail','groupId','qq','content')

class GroupList(admin.ModelAdmin):
    list_display = ('groupName','groupId', 'status')
    search_fields = ('groupName','groupId')

class GroupAdminAdmin(admin.ModelAdmin):
    list_display = ('groupId', 'admin_qq', 'userType')


admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupList)
admin.site.register(GroupAdmin, GroupAdminAdmin)
