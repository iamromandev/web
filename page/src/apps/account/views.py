from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from .mixins import InjectProfileServiceMixin
from .models import Profile
from .serializers import (
    ProfileCreateSerializer,
    ProfileSerializer,
)


# API
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileCreateView(
    InjectProfileServiceMixin,
    generics.CreateAPIView
):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileCreateSerializer

    def perform_create(self, serializer: ProfileCreateSerializer) -> Profile:
        user_id = serializer.validated_data.pop('user_id', None)
        user = self.core_service.get_user_by_id(user_id=user_id)
        profile = serializer.save(user=user)
        logger.info(f"Profile created for user: {user.id}")
        return profile


class ProfileByUserIdApiView(InjectProfileServiceMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer
    queryset = None
    lookup_field = None

    def get_object(self) -> Profile:
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            logger.error("User ID not provided in the request.")
        self.profile_service.get_profile_by_user_id(user_id=user_id)

        return get_object_or_404(self.get_queryset(), user_id=user_id)
