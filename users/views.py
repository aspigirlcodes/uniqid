import logging
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .forms import RegisterForm, SetPasswordConfirmForm, \
                   EmailAuthenticationForm, default_token_generator


logger = logging.getLogger('users')


class PasswordChangeView(UserPassesTestMixin, auth_views.PasswordChangeView):
    template_name = 'users/pwchange.html'
    login_url = reverse_lazy("users:login")
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        """
        Before redirecting add password changed successfully message.
        """
        logger.info("user %s successfully changed password",
                    self.request.user.username)
        messages.success(self.request,
                         _("Your password was changed successfully."))
        return super().form_valid(form)

    def test_func(self):
        """
        Access test: a user can only change their password after their
        email has been confirmed.
        """
        if self.request.user.is_authenticated():
            return self.request.user.profile.email_confirmed
        return False


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    View is accessed by a link containing a unique token.
    This token has been sent to the users email address either because they
    have just registered, or because they requested a password reset.

    **form_class**

    :class:`users.forms.SetPasswordConfirmForm`

    **Context**

    ``ispwchange``
        the user is not setting his password for the first time.

    """
    form_class = SetPasswordConfirmForm
    template_name = "users/pwset.html"
    token_generator = default_token_generator
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.user:
            context['ispwchange'] = self.user.profile.email_confirmed
        return context

    def form_valid(self, form):
        """
        Before redirecting to the login form,
        add a success message
        """
        if self.user.profile.email_confirmed:
            logger.info("successfull passwordreset for user %s",
                        self.user.username)
            messages.success(self.request,
                             _("Your password was changed successfully. "
                               "Please log in with your new password."))
        else:
            logger.info("user %s successfully finished registration by "
                        "setting their password", self.user.username)
            messages.success(self.request,
                             _("Thanks for registering. "
                               "You can now log in with your new password."))
        return super().form_valid(form)


class RegisterView(UserPassesTestMixin, auth_views.PasswordResetView):
    """
    Adaptation of the PasswordResetView for registering a user with
    their email address only and sending them a link to confirm their
    email address.

    **form_class**

    :class:`users.forms.RegisterForm`

    """
    form_class = RegisterForm
    template_name = 'users/register.html'
    email_template_name = "users/email_register.html"
    subject_template_name = "users/subject_register.txt"
    token_generator = default_token_generator
    success_url = reverse_lazy("pages:createpage")

    def form_valid(self, form):
        """
        If a new user has been created during this process, redirect to the
        :class:`pages.views.PageCreateView`, otherwise to the email sent view.
        """
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
                               "account in case you want to keep using it."),
                             extra_tags="modal")
            return HttpResponseRedirect(reverse("pages:createpage"))
        else:
            return HttpResponseRedirect(reverse("users:emailsent"))

    def test_func(self):
        """
        Access test: user should not be authenticated yet.
        """
        return not self.request.user.is_authenticated()


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailAuthenticationForm

    def get_success_url(self):
        """
        If there is a redirect_to parameter in either get or post,
        check if it is safe and use this.

        Else: if the user has created pages already, redirect to
        :class:`pages.views.PageListView`, if not, redirect to
        :class:`pages.views.PageCreateView`
        """
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )

        if not url_is_safe:
            if self.request.user.page_set.exists():
                redirect_to = reverse("pages:pagelist")
            else:
                redirect_to = reverse("pages:createpage")
        return redirect_to
