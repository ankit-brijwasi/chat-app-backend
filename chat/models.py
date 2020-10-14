from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="author_messages")
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def recent_messages(self):
        return Message.objects.order_by('-sent_on').all()[:30]
