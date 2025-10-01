# reactions/urls.py
from django.urls import path
from .views import ReactionListView, ReactionCreateUpdateView, ReactionStatsView

urlpatterns = [
    path('<int:video_id>/', ReactionListView.as_view(), name='reaction-list'),
    path('<int:video_id>/react/', ReactionCreateUpdateView.as_view(), name='reaction-create-update'),
    path('<int:video_id>/stats/', ReactionStatsView.as_view(), name='reaction-stats'),
]
