from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Each user has one profile containing extra information.

    email_confirmed field indicates whether the user has already confirmed
    their email address.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Each time when creating a user, also create a :class:`users.models.Profile`
    """
    if created:
        Profile.objects.create(user=instance)
