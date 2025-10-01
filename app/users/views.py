# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSignupView(generics.CreateAPIView):
    """회원가입 API"""
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    """로그인 API (JWT 발급)"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        })


class UserProfileView(generics.RetrieveAPIView):
    """로그인한 사용자 정보 조회"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
