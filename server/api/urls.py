__author__ = 'jobin'

from django.conf.urls import url

from .controller import user, group, hr


urlpatterns = [
    url(r'^$', user.index.Index.as_view()),
    url(r'^index/', user.index.Index.as_view()),
    url(r'^list/', hr.list.List.as_view()),
    url(r'^reg/', user.reg.Reg.as_view()),
    url(r'^login/', user.login.Login.as_view()),
    url(r'^logout/', user.logout.Logout.as_view()),
    url(r'^check_login/', user.check_login.CheckLogin.as_view()),
    url(r'^change_pwd/', user.change_pwd.ChangePwd.as_view()),
    url(r'^resumes_list/', user.resumes_list.Index.as_view()),
    url(r'^groups_list/', user.groups_list.Index.as_view()),

    url(r'^group/admin_list/', group.admin_list.Index.as_view()),
    url(r'^group/auth_code/', group.auth_code.Index.as_view()),
    url(r'^group/change_pwd/', group.change_pwd.Index.as_view()),
    url(r'^group/check_login/', group.check_login.Index.as_view()),
    url(r'^group/join/', group.join.Index.as_view()),
    url(r'^group/login/', group.login.Index.as_view()),
    url(r'^group/logout/', group.logout.Index.as_view()),
    url(r'^group/resume_list/', group.resume_list.Index.as_view()),
]