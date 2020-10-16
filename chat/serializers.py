from rest_framework.serializers import ModelSerializer
from core.serializers import UserSerializer
from . import models


class RoomSerializer(ModelSerializer):
    admins = UserSerializer(many=True)
    members = UserSerializer(many=True)
    join_requests = UserSerializer(many=True)

    class Meta:
        model = models.Room
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Message
        fields = "__all__"
