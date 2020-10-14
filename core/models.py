from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

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


post_save.connect(create_profile, sender=User)
