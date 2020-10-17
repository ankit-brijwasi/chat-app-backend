from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} profile"


def create_profile(sender, **kwargs):
    instance = kwargs.get('instance')
    if kwargs.get('created'):
        Profile.objects.create(user=instance)


@receiver(user_logged_in)
def user_online(sender, user, request, **kwargs):
    profile = Profile.objects.get(user=user)
    profile.online = True
    profile.save()

    # user.profile.online = True
    # user.save()


@receiver(user_logged_out)
def user_offline(sender, user, request, **kwargs):
    profile = Profile.objects.get(user=user)
    profile.online = False
    profile.save()

    # user.profile.online = False
    # user.save()


post_save.connect(create_profile, sender=User)
