from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from loguru import logger
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from apps.core.models import User
from apps.core.utils.dict_utils import get_sub_dict

from .constants import REGISTRATION_DATA_FIELDS
from .mixins import InjectAuthServiceMixin
from .serializers import RegistrationSerializer
from .services.auth_service import AuthService


class RegistrationView(InjectAuthServiceMixin, generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = None  # User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        logger.debug(f"Calling Registration POST: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Registration Error: {serializer.errors}")
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data = get_sub_dict(serializer.validated_data, REGISTRATION_DATA_FIELDS)
            logger.debug(f"Registration Data: {data}")
            data = self.auth_service.register(
                self.request, **data
            )
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as error:
            logger.error(f"Registration Error: {error}")
            return Response(
                {'error': 'An unexpected error occurred during registration.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyEmailView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, pkb64: str, token: str) -> Response:
        self.auth_service.verify_email(pkb64, token)
        return Response(
            {'detail': 'Email verified successfully.'},
            status=status.HTTP_200_OK
        )


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_data = AuthService.login(
            username=request.data['username'],
            password=request.data['password']
        )
        if login_data:
            return Response(login_data)
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProtectedView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        content = {
            'message': 'This is a protected view, only accessible with a valid token.'
        }
        return Response(content)
