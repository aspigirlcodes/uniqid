"""users URL Configuration

* login/ uses :class:`users.views.LoginView`
* logout/
* resetpassword/
* emailsent/
* setpassword with token, uses :class:`users.views.PasswordResetConfirmView`
* register uses :class:`users.views.RegisterView`
* changepassword (for logged in user),
  uses :class:`users.views.PasswordChangeView`

"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import PasswordResetConfirmView, RegisterView, PasswordChangeView,\
                   LoginView
from .forms import default_token_generator


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(), name="logout"),
    url(r'^resetpassword/$',
        auth_views.PasswordResetView.as_view(
            template_name='users/pwreset.html',
            email_template_name="users/email_pwreset.html",
            subject_template_name="users/subject_pwreset.txt",
            token_generator=default_token_generator,
            success_url="/users/emailsent/"),
        name="resetpw"),
    url(r'^emailsent/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/emailsent.html'),
        name="emailsent"),
    url(r'^setpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name="setpw"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^changepassword/$', PasswordChangeView.as_view(), name="changepw")
]
