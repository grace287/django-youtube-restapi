# comments/urls.py
from django.urls import path
from .views import CommentListView, CommentCreateView, CommentUpdateDeleteView

urlpatterns = [
    path('<int:video_id>/', CommentListView.as_view(), name='comment-list'),
    path('<int:video_id>/create/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/update/', CommentUpdateDeleteView.as_view(), name='comment-update'),
    path('<int:pk>/delete/', CommentUpdateDeleteView.as_view(), name='comment-delete'),
]
