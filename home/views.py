from django.utils import translation
from django.shortcuts import redirect
from django.views.generic import ListView

from pages.models import Page
# Create your views here.


def switch_lang(request, lang):
    """
    Sets the language and redirects.

    This view gets the requested language from a url parameter.
    And the page to redirect to after setting the language
    from the urls get parameters.
    The language sessions key is stored in the requests session.
    """
    redirect_to = request.GET.get("redirect_to", "/")
    if redirect_to == "" or not redirect_to.startswith('/'):
        redirect_to = "/"
    if translation.check_for_language(lang):
        translation.activate(lang)
        if hasattr(request, 'session'):
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
        # else:
        #     response.set_cookie(
        #         settings.LANGUAGE_COOKIE_NAME, lang,
        #         max_age=settings.LANGUAGE_COOKIE_AGE,
        #         path=settings.LANGUAGE_COOKIE_PATH,
        #         domain=settings.LANGUAGE_COOKIE_DOMAIN,
        #     )
    return redirect(redirect_to)


class ExampleListView(ListView):
    model = Page
    template_name = "home/examples.html"

    def get_queryset(self):
        return super().get_queryset().filter(is_example=True,
                                             is_active=True)
