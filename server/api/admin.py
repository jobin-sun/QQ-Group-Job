from django.contrib import admin

# Register your models here.

from .models import User, Resume, AuthCode, Group, GroupMember

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('groupID','adminName', 'code', 'times')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','qq')
    search_fields = ('email', 'username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('userEmail','groupID','qq','display', 'rank')
    search_fields = ('userEmail','groupID','qq','content')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('groupName','groupID','adminName','userType', 'requestMsg', 'status')
    search_fields = ('groupName','groupID','adminName','userType', 'requestMsg')

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('userEmail','groupID','status')
    search_fields = ('userEmail','groupID','status')

admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
