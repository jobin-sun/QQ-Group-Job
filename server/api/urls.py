__author__ = 'jobin'

from django.conf.urls import url

from .controller import user, group, hr


urlpatterns = [
    url(r'^$', user.index.Index.as_view()),
    url(r'^index/', user.index.Index.as_view()),
    url(r'^reg/', user.reg.Reg.as_view()),
    url(r'^login/', user.login.Login.as_view()),
    url(r'^logout/', user.logout.Logout.as_view()),
    url(r'^check_login/', user.check_login.CheckLogin.as_view()),
    url(r'^change_pwd/', user.change_pwd.ChangePwd.as_view()),
    url(r'^resumes_list/', user.resumes_list.Index.as_view()),
    url(r'^groups_list/', user.groups_list.Index.as_view()),
    url(r'^resume/', user.resume.Index.as_view()),
    url(r'^send_activate_mail/', user.mail.Activate.as_view()),
    url(r'^send_recover_mail/', user.mail.Recover.as_view()),
    url(r'^activate/', user.activate.Activate.as_view()),
    url(r'^recover/', user.recover.Recover.as_view()),

    url(r'^group/admin_list/', group.admin_list.Index.as_view()),
    url(r'^group/auth_code/', group.auth_code.Index.as_view()),
    url(r'^group/change_pwd/', group.change_pwd.Index.as_view()),
    url(r'^group/check_login/', group.check_login.Index.as_view()),
    url(r'^group/join/', group.join.Index.as_view()),
    url(r'^group/login/', group.login.Index.as_view()),
    url(r'^group/logout/', group.logout.Index.as_view()),
    url(r'^group/resume_list/', group.resume_list.Index.as_view()),
    url(r'^group/resume/', group.resume.Index.as_view()),
    url(r'^group/send_activate_mail/', group.mail.Activate.as_view()),
    url(r'^group/send_recover_mail/', group.mail.Recover.as_view()),
    url(r'^group/activate/', group.activate.Activate.as_view()),
    url(r'^group/recover/', group.recover.Recover.as_view()),
    url(r'^group/admin/', group.admin.Index.as_view()),

    url(r'^hr/list/', hr.list.List.as_view()),
    url(r'^hr/resume/', hr.resume.Index.as_view()),
]
