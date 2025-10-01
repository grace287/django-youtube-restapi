# reactions/serializers.py
from rest_framework import serializers
from .models import Reaction
from users.serializers import UserInfoSerializer
from videos.serializers import VideoListSerializer


class ReactionSerializer(serializers.ModelSerializer):
    """반응 조회용 Serializer"""
    user = UserInfoSerializer(read_only=True)
    video = VideoListSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'user', 'video', 'reaction', 'created_at', 'updated_at']


class ReactionCreateUpdateSerializer(serializers.ModelSerializer):
    """반응 생성/수정 Serializer"""
    class Meta:
        model = Reaction
        fields = ['video', 'reaction']
