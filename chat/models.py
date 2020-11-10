from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Room(models.Model):
    admins = models.ManyToManyField(
        to=User, blank=True, related_name="admins_room")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    members = models.ManyToManyField(
        to=User, blank=True, related_name="members_room")
    join_requests = models.ManyToManyField(
        to=User, blank=True, related_name="join_requests_room")
    is_public = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=250, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.name)
            num = 1
            while Room.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slugify(self.name), num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_messages")
    room = models.ForeignKey(
        to=Room, default=40, on_delete=models.CASCADE, related_name="room_messages")
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def recent_messages(self):
        return Message.objects.order_by('-sent_on').all()[:30]
