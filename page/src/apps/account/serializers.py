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

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
