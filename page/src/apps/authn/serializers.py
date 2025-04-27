from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.core.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            'username',
            'email',
            'password',
            'password2',
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        refresh_token_str: str = attrs.get("refresh_token")
        if not refresh_token_str:
            raise serializers.ValidationError({"refresh_token": "This field is required."})

        try:
            refresh = RefreshToken(refresh_token_str)
            access_token = refresh.access_token
        except TokenError as e:
            raise AuthenticationFailed(
                f"Invalid token: {str(e)}", code="token_not_valid"
            )

        return {
            "access_token": str(access_token),
        }
