# comments/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Comment
from videos.models import Video
from .serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer


class CommentListView(generics.ListAPIView):
    """특정 비디오의 댓글 목록"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        video_id = self.kwargs["video_id"]
        return Comment.objects.filter(video_id=video_id).order_by("-created_at")


class CommentCreateView(generics.CreateAPIView):
    """댓글 작성"""
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        video = get_object_or_404(Video, id=self.kwargs["video_id"])
        serializer.save(user=self.request.user, video=video)


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """댓글 수정/삭제"""
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CommentUpdateSerializer
        return CommentSerializer

    def perform_update(self, serializer):
        # 작성자만 수정 가능
        if self.get_object().user != self.request.user:
            raise PermissionError("본인이 작성한 댓글만 수정할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError("본인이 작성한 댓글만 삭제할 수 있습니다.")
        instance.delete()
