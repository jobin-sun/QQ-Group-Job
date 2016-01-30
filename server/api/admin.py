from django.contrib import admin

# Register your models here.

from .models import User, Resume, AuthCode, Group

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('groupID','adminName', 'code', 'times')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','qq')
    search_fields = ('email', 'username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('userEmail','groupID','qq','display')
    search_fields = ('userEmail','groupID','qq','content')

class GroupList(admin.ModelAdmin):
    list_display = ('groupName','groupID','requestMsg', 'status')
    search_fields = ('groupName','groupID', 'requestMsg')


admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupList)
