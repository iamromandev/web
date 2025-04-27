
from rest_framework import serializers

from apps.core.models import User

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
