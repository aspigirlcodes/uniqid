from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, SetPasswordConfirmForm


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = SetPasswordConfirmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user:
            context['ispwchange'] = self.user.profile.email_confirmed
        return context

    def form_valid(self, form):
        if self.user.profile.email_confirmed:
            messages.success(self.request,
                             _("Your password was changed successfully. "
                               "Please log in with your new password."))
        else:
            messages.success(self.request,
                             _("Thanks for registering. "
                               "You can now log in with your new password."))
        return super().form_valid(form)


class RegisterView(auth_views.PasswordResetView):
    form_class = RegisterForm

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        created = form.save(**opts)
        if created:
            # todo add message
            return HttpResponseRedirect(reverse("pages:createpage"))
        else:
            return HttpResponseRedirect(reverse("users:emailsent"))
