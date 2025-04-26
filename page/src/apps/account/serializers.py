
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

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


# class TokenRefreshSerializer(_TokenRefreshSerializer):
#     def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
#         data = super().validate(attrs)
#         data['access_token'] = data.get('access_token')
#         if data['access_token']:
#             access_token = AccessToken(data['access_token'])
#
#         return data
