from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    def form_valid(self, form):
        messages.success(self.request,
                         _("Your password was changed successfully. "
                           "Please log in with your new password."))
        return super().form_valid(form)
