from typing import Optional

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import User

from ..repos.user_repo import UserRepo


class AuthService:
    @staticmethod
    def register(
        username: str, email: str, password: str, password2: str
    ) -> dict:
        if password != password2:
            return {"error": "Passwords do not match"}

        user: User = UserRepo.create_user(username, email, password)
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
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

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
