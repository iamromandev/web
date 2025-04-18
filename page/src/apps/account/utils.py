from django.contrib.auth.tokens import default_token_generator

from apps.core.models import User


class RegistrationUtils:
    @staticmethod
    def generate_email_verification_token(user: User) -> str:
        return default_token_generator.make_token(user)
