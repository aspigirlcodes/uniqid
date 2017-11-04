from django.utils import translation
from django.shortcuts import redirect

# Create your views here.


def switch_lang(request, lang):
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
