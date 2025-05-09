
from django.core.exceptions import ObjectDoesNotExist

from apps.account.models import Profile
from apps.core.models import User
from apps.core.repos.base_repo import BaseRepo


class ProfileRepo(BaseRepo[Profile]):

    def __init__(self):
        super().__init__(Profile)

    def get_profile_by_user(self, user: User) -> Profile | None:
        try:
            profile = Profile.objects.get(user=user)
            return profile
        except ObjectDoesNotExist:
            return None
