# subscriptions/urls.py
from django.urls import path
from .views import SubscriptionListView, SubscriberListView, SubscriptionCreateDeleteView

urlpatterns = [
    path('my-subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('my-subscribers/', SubscriberListView.as_view(), name='subscriber-list'),
    path('toggle/', SubscriptionCreateDeleteView.as_view(), name='subscription-toggle'),
]
