from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, SetPasswordConfirmForm


class PasswordChangeView(UserPassesTestMixin, auth_views.PasswordChangeView):
    def test_func(self):
        if self.request.user.is_authenticated():
            return self.request.user.profile.email_confirmed
        return False

    def form_valid(self, form):
        messages.success(self.request,
                         _("Your password was changed successfully."))
        return super().form_valid(form)


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


class RegisterView(UserPassesTestMixin, auth_views.PasswordResetView):
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
            messages.success(self.request,
                             _("You can now start creating your page. "
                               "We've sent you an email to confirm your "
                               "account in case you want to keep using it."))
            return HttpResponseRedirect(reverse("pages:createpage"))
        else:
            return HttpResponseRedirect(reverse("users:emailsent"))

    def test_func(self):
        return not self.request.user.is_authenticated()
