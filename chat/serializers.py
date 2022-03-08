from rest_framework import serializers
from .models import User, Chat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' ,'name')

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id' ,'user_1', 'user_2')
