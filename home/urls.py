"""Home app URL Configuration

i18n/set-lang/<lang>
    Changes the language and redirects back
    to the current view. Supported languages are English and German.
how/
    Directs to a static page with an in depth explanation of how to use
    the app. (currently empty)
why/
    Directs to a static page with reasons why the app could be usefull.
    (currently empty)
faq/
    Static page with frequently asked questions. (currently empty)
about/
    Information about the project. (currently empty)
examples/
    Some examples of what finished pages could look like.
/
    The homepage.
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import switch_lang, ExampleListView

urlpatterns = [
    url(r'^i18n/set-lang/(?P<lang>\w{2})/', switch_lang, name="switch_lang"),
    url(r'^how/', TemplateView.as_view(template_name='pages/empty.html'),
        name="how"),
    url(r'^why/', TemplateView.as_view(template_name='pages/empty.html'),
        name="why"),
    url(r'^faq/', TemplateView.as_view(template_name='home/faq.html'),
        name="faq"),
    url(r'^about/', TemplateView.as_view(template_name='pages/empty.html'),
        name="about"),
    url(r'^examples/', ExampleListView.as_view(),
        name="examples"),
    url(r'^', TemplateView.as_view(template_name='home/home.html'),
        name="home"),
]
