__author__ = 'jobin'

from django.conf.urls import url

from .controller import user, group, hr


urlpatterns = [
    url(r'^$', user.index.Index.as_view()),
    url(r'^index/', user.index.Index.as_view()),
    url(r'^list/', hr.list.List.as_view()),
    url(r'^profile/', hr.profile.Profile.as_view()),
    url(r'^reg/', user.reg.Reg.as_view()),
    url(r'^login/', user.login.Login.as_view()),
    url(r'^logout/', user.logout.Logout.as_view()),
    url(r'^check_login/', user.check_login.CheckLogin.as_view()),
    url(r'^change_pwd/', user.change_pwd.ChangePwd.as_view()),
]