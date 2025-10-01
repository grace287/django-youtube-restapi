# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """기본 User 정보 직렬화"""
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_active']


class UserSignupSerializer(serializers.ModelSerializer):
    """회원가입 Serializer"""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

class UserInfoSerializer(serializers.ModelSerializer):
    """영상/댓글 등에서 참조용으로 간단히 유저 정보만 직렬화"""
    class Meta:
        model = User
        fields = ['id', 'email']

class UserLoginSerializer(serializers.Serializer):
    """로그인 Serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
        attrs["user"] = user
        return attrs
