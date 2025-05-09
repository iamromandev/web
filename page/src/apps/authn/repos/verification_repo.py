
from django.core.exceptions import ObjectDoesNotExist

from apps.core.models import User
from apps.core.repos.base_repo import BaseRepo

from ..models import Verification


class VerificationRepo(BaseRepo[Verification]):
    def __init__(self):
        super().__init__(Verification)

    def get_by_user(self, user: User) -> Verification | None:
        try:
            verification = Verification.objects.get(user=user)
            return verification
        except ObjectDoesNotExist:
            return None
