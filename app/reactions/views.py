# reactions/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Reaction
from videos.models import Video
from .serializers import ReactionSerializer, ReactionCreateUpdateSerializer


class ReactionListView(generics.ListAPIView):
    """특정 영상의 리액션 목록"""
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        video_id = self.kwargs.get("video_id")
        return Reaction.objects.filter(video_id=video_id)


class ReactionCreateUpdateView(generics.CreateAPIView):
    """좋아요/싫어요 등록 및 수정"""
    serializer_class = ReactionCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        reaction, created = Reaction.objects.get_or_create(
            user=request.user, video=video
        )

        serializer = self.get_serializer(reaction, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Reaction saved", "reaction": serializer.data},
            status=status.HTTP_200_OK
        )


class ReactionStatsView(generics.RetrieveAPIView):
    """특정 영상의 좋아요/싫어요 개수 반환"""
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        stats = Reaction.get_video_reactions(video)
        return Response(stats)
