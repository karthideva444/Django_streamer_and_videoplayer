from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class VideoSerializer(serializers.ModelSerializer):
    uploader_username = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Video
        fields = ['id', 'name', 'video_url', 'uploader_username']