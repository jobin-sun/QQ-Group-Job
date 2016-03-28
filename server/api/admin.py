from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.

from .models import User, Resume, AuthCode, Group, GroupAdmin, Rank
from .send_mail import start_mail_thread
from api.config import email_address, admin_email, admin_group
from QQJob.settings import BASE_DIR

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
    list_display = ('id','resumeId', 'groupId', 'qq','rank')
    search_fields = ('id','resumeId','qq')

    def groupId(self, obj):
        try:
            groupId = Resume.objects.get(groupId__exact =obj.resumeId).groupId
            return groupId
        except ObjectDoesNotExist:
            return u'无群号简历'

class GroupAdminAdmin(admin.ModelAdmin):
    list_display = ('id','groupId', 'qq', 'userType')
    search_fields = ('id','groupId', 'qq')

class GroupListAdmin(admin.ModelAdmin):
    actions = ['delete_model']
    list_display = ('id','groupName','groupId', 'owner', 'status', 'activate')
    search_fields = ('id','groupName','groupId')

#    def get_actions(self, request):
#        actions = super(GroupListAdmin, self).get_actions(request)
#        del actions['delete_selected']
#        return actions

    def delete_selected(self, request, queryset):
        for obj in queryset:
            try:
                resumes = Resume.objects.filter(groupId__exact = obj.groupId).all()
                resumes.delete()
                ranks = Rank.objects.filter(groupId__exact = obj.groupId).all()
                ranks.delete()
                authcode = AuthCode.objects.filter(groupId__exact = obj.groupId).all()
                authcode.delete()
                receiver = GroupAdmin.objects.get(groupId__exact =obj.groupId, userType__exact=1)
                admins = GroupAdmin.objects.filter(groupId__exact =obj.groupId).all()
                admins.delete()
            except ObjectDoesNotExist:
                pass
            with open(BASE_DIR + "/api/mail_template/checkGroupFail.html", 'rt', encoding='utf-8') as mail_template:
                template = mail_template.read()
            email_content = template % (obj.groupId, admin_email, admin_group)
            obj.delete()
            start_mail_thread(
                u'Qjob 审核失败',
                email_content,
                email_address,
                ['%s@qq.com' % receiver.qq]
            )
    delete_selected.short_description = 'Delete Groups'

    def owner(self, obj):
        try:
            admin = GroupAdmin.objects.get(groupId__exact =obj.groupId, userType__exact=1)
        except ObjectDoesNotExist:
            return ''
        return admin.qq

    def activate(self, obj):
        activate = (u'未激活',u'已激活')
        try:
            status = GroupAdmin.objects.get(groupId__exact =obj.groupId, userType__exact=1).status
            return activate[status]
        except ObjectDoesNotExist:
            return ''



admin.site.register(User, UserAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Rank, RankAdmin)
admin.site.register(AuthCode, AuthCodeAdmin)
admin.site.register(Group, GroupListAdmin)
admin.site.register(GroupAdmin, GroupAdminAdmin)
