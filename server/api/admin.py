from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

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

class GroupAdminAdmin(admin.ModelAdmin):
    list_display = ('groupId', 'adminName', 'userType')

class GroupListAdmin(admin.ModelAdmin):
    actions = ['delete_model']
    list_display = ('groupName','groupId', 'owner', 'requestMsg', 'status')
    search_fields = ('groupName','groupId', 'requestMsg')
    fields = ('groupName','groupId', 'requestMsg', 'status')
    def get_actions(self, request):
        actions = super(GroupListAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    def delete_model(self, request, obj):
        for o in obj.all():
            o.delete()
    delete_model.short_description = 'Delete Groups'

    def owner(self, obj):
        try:
            admin = GroupAdmin.objects.get(groupId__exact =obj.groupId, userType__exact=1)
        except ObjectDoesNotExist:
            return ''
        return admin.adminName


admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupListAdmin)
admin.site.register(GroupAdmin, GroupAdminAdmin)
