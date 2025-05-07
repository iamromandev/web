from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import QuerySet
from loguru import logger
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView as _TokenRefreshView

from apps.core.libs import Error, PasswordMismatchError, Resp, Success
from apps.core.mixins import InjectCoreMixin, InjectUserServiceMixin
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
    queryset: Optional[QuerySet] = None
    serializer_class = RegistrationSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        logger.debug(f"Calling Registration POST: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error||Registration Serializer: {serializer.errors}")
            error = Error(
                status=Resp.Status.ERROR,
                code=Resp.Code.BAD_REQUEST,
                type=Error.Type.UNIQUE_CONSTRAINT_VIOLATION,
                details=serializer.errors,
            )
            return error.to_resp()

        try:
            data = get_sub_dict(serializer.validated_data, REGISTRATION_DATA_FIELDS)
            logger.debug(f"Registration Data: {data}")
            self.auth_service.register(
                self.request, **data
            )
            success = Success(
                status=Resp.Status.SUCCESS,
                code=Resp.Code.OK,
                message=MESSAGE_REGISTRATION_SUCCESS
            )
            return success.to_resp()
        except PasswordMismatchError as error:
            logger.error(f"PasswordMismatchError||Registration: {error}")
            return error.to_resp()
        except Exception as error:
            logger.error(f"Error||Registration: {error}")
            error = Error(
                code=Resp.Code.INTERNAL_SERVER_ERROR,
                type=Error.Type.SERVER_ERROR,
                details=error,
            )
            return error.to_resp()


class VerifyEmailView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request, pkb64: str, token: str) -> Response:
        response = self.auth_service.verify_email(pkb64, token)
        success = Success(
            data=response
        )
        return success.to_resp()


class LoginView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error||Login Serializer: {serializer.errors}")
            error = Error(
                code=Resp.Code.BAD_REQUEST,
                type=Error.Type.UNIQUE_CONSTRAINT_VIOLATION,
                details=serializer.errors,
            )
            return error.to_resp()

        data = get_sub_dict(serializer.validated_data, LOGIN_DATA_FIELDS)
        logger.debug(f"Login Data: {data}")
        resp = self.auth_service.login(**data)

        success = Success(
            status=Resp.Status.SUCCESS,
            code=Resp.Code.OK,
            data=resp
        )
        return success.to_resp()


class TokenView(InjectAuthServiceMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error||Token Serializer: {serializer.errors}")
            error = Error(
                code=Resp.Code.BAD_REQUEST,
                type=Error.Type.UNIQUE_CONSTRAINT_VIOLATION,
                details=serializer.errors,
            )
            return error.to_resp()

        data = get_sub_dict(serializer.validated_data, TOKEN_DATA_FIELDS)
        logger.debug(f"Token Data: {data}")
        resp = self.auth_service.token(**data)

        success = Success(
            status=Resp.Status.SUCCESS,
            code=Resp.Code.OK,
            data=resp
        )
        return success.to_resp()


class TokenRefreshView(InjectAuthServiceMixin, _TokenRefreshView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Error||Token Refresh Serializer: {serializer.errors}")
            error = Error(
                code=Resp.Code.BAD_REQUEST,
                type=Error.Type.UNIQUE_CONSTRAINT_VIOLATION,
                details=serializer.errors,
            )
            return error.to_resp()

        data = serializer.validated_data
        data = get_sub_dict(data, TOKEN_REFRESH_DATA_FIELDS)
        resp = self.auth_service.token_refresh(data.get("refresh_token"))

        logger.debug(f"Token Refresh Data: {resp}")
        success = Success(
            data=resp
        )
        return success.to_resp()
