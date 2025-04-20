from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)
from loguru import logger
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import User

from ..models import Verification
from ..repos.profile_repo import ProfileRepo
from ..repos.user_repo import UserRepo
from ..repos.verification_repo import VerificationRepo


class AuthService:

    def __init__(
        self,
        user_repo: Optional[UserRepo] = None,
        profile_repo: Optional[ProfileRepo] = None,
        verification_repo: Optional[VerificationRepo] = None,
    ):
        self.user_repo = user_repo or UserRepo()
        self.profile_repo = profile_repo or ProfileRepo()
        self.verification_repo = verification_repo or VerificationRepo()

    def _create_verification_pkb64_token(self, user: User) -> tuple[str, str]:
        pk_bytes = force_bytes(user.pk)
        pkb64 = urlsafe_base64_encode(pk_bytes)
        token = default_token_generator.make_token(user)
        return pkb64, token

    def _restore_pk(self, pkb64: str) -> str:
        pk_bytes = urlsafe_base64_decode(pkb64)
        pk = force_str(pk_bytes)
        return pk

    def _create_verification_url(self, request: Request, user: User) -> str:
        pkb64, token = self._create_verification_pkb64_token(user)
        verification_url = request.build_absolute_uri(
            reverse("verify_email", kwargs={"pkb64": pkb64, "token": token})
        )
        return verification_url

    def register(
        self, request: Request, username: str, email: str, password: str, password2: str
    ) -> dict:
        if password != password2:
            return {"error": "Passwords do not match"}

        # if self.user_repo.exists(email=email):
        #    raise ValueError("Email address already exists.")

        user: User = self.user_repo.create(
            username=username,
            email=email,
            password=make_password(password),
            is_active=False,
        )
        self.profile_repo.create(user=user)
        self.verification_repo.create(
            user=user,
            type=Verification.Type.EMAIL,
            status=Verification.Status.PENDING,
        )

        verification_url = self._create_verification_url(request, user)
        # TODO - Use a proper email template
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

    def verify_email(
        self, pkb64: str, token: str
    ) -> dict:
        try:
            pk = self._restore_pk(pkb64)
            user = self.user_repo.get_by_pk(pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error("Invalid verification link")
            user = None

        if user and default_token_generator.check_token(user, token):
            self.user_repo.update(user, is_active=True)
            verification: Optional[Verification] = self.verification_repo.get_by_user(user)
            if verification and verification.is_verified:
                logger.info(f"User {user.email} already verified.")
                return {"detail": "Email already verified"}
            else:
                self.verification_repo.update(
                    verification,
                    status=Verification.Status.VERIFIED
                )
                return {"detail": "Email verified successfully"}

        return {"error": "Invalid verification link"}

    def login(
        self, username: str, password: str
    ) -> dict:
        # Check if the user exists and is active
        user: Optional[User] = authenticate(username=username, password=password)
        logger.info(f"User {user} attempted to log in.")
        if not user:
            return {"error": "User not found"}

        if not user.check_password(password):
            return {"error": "Invalid password"}

        verification: Optional[Verification] = self.verification_repo.get_by_user(user)
        if not verification or not verification.is_verified:
            return {"error": "Email not verified"}
        
        refresh = RefreshToken.for_user(user)
        logger.info(f"User {user.username} logged in successfully.")
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'detail': 'Login successful.'
        }
