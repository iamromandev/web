from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import User

from ..repos.user_repo import UserRepo


class AuthService:
    @staticmethod
    def register(
        request: Request,
        username: str, email: str, password: str, password2: str
    ) -> dict:
        if password != password2:
            return {"error": "Passwords do not match"}

        user = UserRepo.create_user(username, email, password)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_url = request.build_absolute_uri(
            reverse("verify_email", kwargs={"uidb64": uid, "token": token})
        )
        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify your email: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'detail': 'Registration successful. '
                      'Please check your email to verify your account.'
        }

    @staticmethod
    def login(
        username: str, password: str
    ) -> dict:
        user: Optional[User] = authenticate(username=username, password=password)
        if not user:
            return {"error": "User not found"}

        if not user.check_password(password):
            return {"error": "Invalid password"}

        return {
            "refresh": "str(refresh)",
            "access": "str(refresh.access_token)",
        }
