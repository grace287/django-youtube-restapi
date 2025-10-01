# comments/serializers.py
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    video = serializers.ReadOnlyField(source="video.id")

    class Meta:
        model = Comment
        fields = ["id", "user", "video", "content", "like", "dislike", "created_at", "updated_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]

    def create(self, validated_data):
        user = self.context["request"].user
        video = self.context["video"]
        return Comment.objects.create(user=user, video=video, **validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]
