"""uniqid URL Configuration

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
from django.views.generic import TemplateView
from .views import switch_lang

urlpatterns = [
    url(r'^i18n/set-lang/(?P<lang>\w{2})/', switch_lang, name="switch_lang"),
    url(r'^how/', TemplateView.as_view(template_name='pages/empty.html'),
        name="how"),
    url(r'^why/', TemplateView.as_view(template_name='pages/empty.html'),
        name="why"),
    url(r'^faq/', TemplateView.as_view(template_name='pages/empty.html'),
        name="faq"),
    url(r'^about/', TemplateView.as_view(template_name='pages/empty.html'),
        name="about"),
    url(r'^examples/',
        TemplateView.as_view(template_name='home/examples.html'),
        name="examples"),
    url(r'^', TemplateView.as_view(template_name='home/home.html'),
        name="home"),
]
