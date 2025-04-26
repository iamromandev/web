from typing import Any

from django.contrib.auth.password_validation import validate_password
from loguru import logger
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as _TokenRefreshSerializer,
)

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


class TokenRefreshSerializer(_TokenRefreshSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"TokenRefreshSerializer.validate: {attrs}")
        if 'refresh_token' in attrs:
            attrs['refresh'] = attrs.pop('refresh_token')
        data = super().validate(attrs)
        #if 'refresh' in data:
        #    data['refresh_token'] = data.pop('refresh')

        return data
