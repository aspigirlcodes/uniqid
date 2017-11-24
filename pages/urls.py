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
# from django.views.generic import TemplateView
from .views import GeneralInfoModuleCreateView, PageCreateView,\
                   FreeTextModuleCreateView, SelectModuleView, PagePreview,\
                   FreeListModuleCreateView

urlpatterns = [
    url(r'^createpage/$', PageCreateView.as_view(), name="createpage"),
    # url(r'^createpage/',
    #     TemplateView.as_view(template_name='pages/empty.html'),
    #     name="createpage"),
    url(r'^(?P<pk>[0-9]+)/addmodule/$',
        SelectModuleView.as_view(), name="addmodule"),
    url(r'^(?P<page_id>[0-9]+)/creategeneralinfomodule/$',
        GeneralInfoModuleCreateView.as_view(), name="creategeneralinfomodule"),
    url(r'^(?P<page_id>[0-9]+)/createfreetextmodule/$',
        FreeTextModuleCreateView.as_view(), name="createfreetextmodule"),
    url(r'^(?P<page_id>[0-9]+)/createfreelistmodule/$',
        FreeListModuleCreateView.as_view(), name="createfreelistmodule"),
    url(r'^(?P<pk>[0-9]+)/preview/$',
        PagePreview.as_view(), name="pagepreview"),
]
