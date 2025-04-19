from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from loguru import logger
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from apps.core.models import User
from apps.core.utils.dict_utils import get_sub_dict

from .constants import REGISTRATION_DATA_FIELDS
from .serializers import RegistrationSerializer
from .services.auth_service import AuthService


class RegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     token = default_token_generator.make_token(user)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     verification_url = self.request.build_absolute_uri(
    #         reverse("verify_email", kwargs={"uidb64": uid, "token": token})
    #     )
    #     send_mail(
    #         subject="Verify your email",
    #         message=f"Click the link to verify your email: {verification_url}",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[user.email],
    #         fail_silently=False,
    #     )
    #     return user

    def post(self, request, *args, **kwargs):
        logger.debug(f"Calling Registration POST: {request.data}")
        serializer = self.get_serializer(data=request.data)
        # TODO more control response
        serializer.is_valid(raise_exception=True)
        try:
            data = get_sub_dict(serializer.validated_data, REGISTRATION_DATA_FIELDS)
            logger.debug(f"Registration Data: {data}")
            data = AuthService.register(self.request, **data)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(
                {'error': 'An unexpected error occurred during registration.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # self.perform_create(serializer)
        # return Response(
        #     {
        #         'detail': 'Registration successful. '
        #                   'Please check your email to verify your account.'
        #     },
        #     status=status.HTTP_201_CREATED
        # )


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


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        pass
        # try:
        #     #uid = force_str(urlsafe_base64_decode(uidb64))
        #     #user = User.objects.get(pk=uid)
        # except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        #     user = None
        #
        # if user is not None and default_token_generator.check_token(user, token):
        #     # user.is_email_verified = True
        #     user.is_active = True
        #     user.save()
        #     return Response(
        #         {'detail': 'Email verified successfully. You can now log in.'},
        #         status=status.HTTP_200_OK
        #     )
        # else:
        #     return Response(
        #         {'detail': 'Invalid or expired verification link.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )


class ProtectedView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        content = {
            'message': 'This is a protected view, only accessible with a valid token.'
        }
        return Response(content)
