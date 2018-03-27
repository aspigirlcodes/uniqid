"""uniqid URL Configuration

admin/
    The django admin
i18n/
    Django translation tools
jsi18n/
    The javascript catalog for translations
users/
    urls from the users app
pages/
    urls from the pages app
`/`
    urls from the home app
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^users/',
        include('users.urls', namespace='users', app_name='users')),
    url(r'^pages/',
        include('pages.urls', namespace='pages', app_name='pages'))] +\
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^', include('home.urls', namespace='home', app_name='home'))
]
