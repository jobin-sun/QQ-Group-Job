from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.

from .models import User, Resume, AuthCode, Group, GroupAdmin, Rank

class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ('id','groupId','qq', 'code', 'times')
    search_fields = ('id','groupId', 'qq')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','qq')
    search_fields = ('id','username', 'qq')

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id','userEmail','groupId','qq','display')
    search_fields = ('id','userEmail','groupId','qq','content')

class RankAdmin(admin.ModelAdmin):
    list_display = ('id','resumeId','qq','rank')
    search_fields = ('id','resumeId','qq')

class GroupAdminAdmin(admin.ModelAdmin):
    list_display = ('id','groupId', 'qq', 'userType')
    search_fields = ('id','groupId', 'qq')

class GroupListAdmin(admin.ModelAdmin):
    actions = ['delete_model']
    list_display = ('id','groupName','groupId', 'owner', 'status')
    search_fields = ('id','groupName','groupId')
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
        return admin.qq


admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupListAdmin)
admin.site.register(GroupAdmin, GroupAdminAdmin)
