from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'display_name',
            'bio',
        )
        read_only_fields = ('id',)
