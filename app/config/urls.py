
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # 앱 라우팅
    path('api/v1/users/', include('users.urls')),         # 회원 관련
    path('api/v1/videos/', include('videos.urls')),       # 동영상 관련
    path('api/v1/reactions/', include('reactions.urls')), # 좋아요/싫어요
    path('api/v1/comments/', include('comments.urls')),   # 댓글
    path('api/v1/subscriptions/', include('subscriptions.urls')), # 구독
    
]

