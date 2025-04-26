from typing import Any

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
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

from apps.core.mixins import InjectCoreMixin
from apps.core.models import User
from apps.core.utils.dict_utils import get_sub_dict

from .constants import (
    LOGIN_DATA_FIELDS,
    MESSAGE_REGISTRATION_SUCCESS,
    REGISTRATION_DATA_FIELDS,
    TOKEN_DATA_FIELDS,
    TOKEN_REFRESH_DATA_FIELDS,
)
from .mixins import InjectAuthServiceMixin
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    TokenRefreshSerializer,
    TokenSerializer,
)


class RegistrationView(InjectCoreMixin, InjectAuthServiceMixin, generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = None  # User.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        logger.debug(f"Calling Registration POST: {request.data}")
        rb = self.response_builder
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
            rb.set_message(MESSAGE_REGISTRATION_SUCCESS)
            return rb.build()
        except Exception as error:
            logger.error(f"Registration Error: {error}")
            return Response(
                {'error': 'An unexpected error occurred during registration.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyEmailView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, pkb64: str, token: str) -> Response:
        response = self.auth_service.verify_email(pkb64, token)
        return Response(response, status=status.HTTP_200_OK)


class LoginView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Login data invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = get_sub_dict(serializer.validated_data, LOGIN_DATA_FIELDS)
        logger.debug(f"Login Data: {data}")
        login_data = self.auth_service.login(**data)

        return Response(login_data, status=status.HTTP_200_OK)


class TokenView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Token data invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = get_sub_dict(serializer.validated_data, TOKEN_DATA_FIELDS)
        logger.debug(f"Token Data: {data}")
        token_data = self.auth_service.token(**data)

        return Response(token_data, status=status.HTTP_200_OK)


class TokenRefreshView(InjectAuthServiceMixin, _TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Token refresh data invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        data = get_sub_dict(data, TOKEN_REFRESH_DATA_FIELDS)
        data = self.auth_service.token_refresh(data)

        logger.debug(f"Token Refresh Data: {data}")
        return Response(data, status=status.HTTP_200_OK)


class ProtectedView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        content = {
            'message': 'This is a protected view, only accessible with a valid token.'
        }
        return Response(content)
