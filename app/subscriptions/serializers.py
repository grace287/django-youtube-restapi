# subscriptions/serializers.py
from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.ReadOnlyField(source="subscriber.email")
    subscribed_to = serializers.ReadOnlyField(source="subscribed_to.email")

    class Meta:
        model = Subscription
        fields = ["id", "subscriber", "subscribed_to", "created_at", "updated_at"]


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["subscribed_to"]

    def validate_subscribed_to(self, value):
        user = self.context["request"].user
        if value == user:
            raise serializers.ValidationError("자기 자신은 구독할 수 없습니다.")
        return value
