"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import PasswordResetConfirmView, RegisterView
from .forms import default_token_generator, EmailAuthenticationForm
# from django.views.generic import TemplateView


urlpatterns = [
    url(r'^login/$',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            authentication_form=EmailAuthenticationForm),
        name="login"),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(), name="logout"),
    url(r'^resetpassword/$',
        auth_views.PasswordResetView.as_view(
            template_name='users/pwreset.html',
            email_template_name="users/email_pwreset.html",
            subject_template_name="users/subject_pwreset.txt",
            token_generator=default_token_generator,
            success_url="/users/emailsent/"),
        name="pwreset"),
    url(r'^emailsent/$',
        auth_views.LoginView.as_view(template_name='users/emailsent.html'),
        name="emailsent"),
    url(r'^setpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/"\
        "(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(
            template_name="users/pwset.html",
            token_generator=default_token_generator,
            success_url="/users/login/"
        ),
        name="setpw"),
    url(r'^register/$',
        RegisterView.as_view(
            template_name='users/register.html',
            email_template_name="users/email_register.html",
            subject_template_name="users/subject_register.txt",
            token_generator=default_token_generator,
            success_url="/pages/createpage/"),
        name="register"),
]
