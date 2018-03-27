import logging
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


logger = logging.getLogger('users')


UserModel = get_user_model()


class TokenGenerator(PasswordResetTokenGenerator):
    """
    overwrites _make_hash_value to include :class:`users.models.Profile`
    email_confirmed field.
    """
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
    """
    Addaptation of the PasswordResetForm to use for registering users and
    sending them a one time link to confirm their email address.
    """

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
             subject_template_name="users/subject_register.txt",
             email_template_name="users/email_register.html",
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        If a user with this email address does not exist yet, create one.
        with username and email equal to this email address.

        If the user has not confirmed his email address yet:
        generates a one-use only link for setting password and sends to the
        user.

        Returns whether a user was created or not.
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
            logger.info("new user created: %s", user.username)
        if not user.profile.email_confirmed:
            logger.info("sending email with registration link to user: %s",
                        user.username)
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
        """
        If :class:`users.models.Profile` email_confirmed is False,
        set it to True now. (setting the password confirms the email address)
        """
        user = super().save(commit)
        logger.info("password reset done for user: %s", user.username)
        if not user.profile.email_confirmed:
            logger.info("switching user %s to email confirmed",
                        user.username)
            user.profile.email_confirmed = True
            user.profile.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """
    adds email validation to the username field in the AuthenticationForm
    """
    username = UsernameField(
        max_length=254,
        widget=EmailInput(attrs={'autofocus': True}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].validators.append(EmailValidator())
        self.fields['username'].label = _("Email")
