# subscriptions/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Subscription
from users.models import User
from .serializers import SubscriptionSerializer, SubscriptionCreateSerializer


class SubscriptionListView(generics.ListAPIView):
    """내가 구독한 채널 목록"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)


class SubscriberListView(generics.ListAPIView):
    """나를 구독한 사람 목록"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscribed_to=self.request.user)


class SubscriptionCreateDeleteView(generics.GenericAPIView):
    """구독 추가/취소"""
    serializer_class = SubscriptionCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        subscribed_to = serializer.validated_data["subscribed_to"]

        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            subscribed_to=subscribed_to
        )

        if created:
            return Response({"message": f"{subscribed_to.email} 님을 구독했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "이미 구독 중입니다."}, status=status.HTTP_200_OK)

    def delete(self, request):
        subscribed_to_id = request.data.get("subscribed_to_id")
        subscribed_to = get_object_or_404(User, id=subscribed_to_id)

        subscription = Subscription.objects.filter(
            subscriber=request.user, subscribed_to=subscribed_to
        ).first()

        if subscription:
            subscription.delete()
            return Response({"message": f"{subscribed_to.email} 님의 구독을 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "구독 관계가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
