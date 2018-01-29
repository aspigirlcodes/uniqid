from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, \
                                      AuthenticationForm, UsernameField
from django.contrib.auth import get_user_model, login
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import EmailInput

UserModel = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Ensure results are consistent across DB backends
        login_timestamp = '' if user.last_login is None \
            else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.password +
            six.text_type(login_timestamp) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )


default_token_generator = TokenGenerator()


class RegisterForm(PasswordResetForm):
    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        }).select_related('profile')
        return active_users

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        users = self.get_users(email)
        if users:
            user = users[0]
            created = False
        else:
            user = UserModel.objects.create_user(username=email,
                                                 email=email)
            login(request, user)
            created = True
        if not user.profile.email_confirmed:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(
                subject_template_name, email_template_name, context,
                from_email, email,
                html_email_template_name=html_email_template_name,
            )
        return created


class SetPasswordConfirmForm(SetPasswordForm):
    def save(self, commit=True):
        user = super().save(commit)
        if not user.profile.email_confirmed:
            user.profile.email_confirmed = True
            user.profile.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].validators.append(EmailValidator())
        self.fields['username'].label = _("Email")
