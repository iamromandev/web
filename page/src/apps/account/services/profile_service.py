import uuid
from typing import Optional, Union

from loguru import logger

from apps.account.repos.profile_repo import ProfileRepo
from apps.authn.services.auth_service import AuthService
from apps.core.models import User as _User

from ..models import Profile as _Profile


class ProfileService(AuthService):
    def __init__(
        self,
        profile_repo: Optional[ProfileRepo] = None,
    ) -> None:
        self._profile_repo = profile_repo or ProfileRepo()

    def create_profile(self, user_id: Union[str, uuid.UUID]) -> _Profile:
        user_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        user: Optional[_User] = self.user_repo.get_by_pk(pk=user_id)
        logger.info(f"Create Profile > User: {user}")
        profile: _Profile = self._profile_repo.create_profile(user=user)
        return profile

    # calling by view of another app using ApiClient
    def get_profile(self) -> None:
        self.user_repo.get_user_by_username(self._username)
        pass

    # this is calling for building api of profile
    def get_profile_by_user_id(self, user_id: Union[str, uuid.UUID]) -> Optional[_Profile]:
        user_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        user: Optional[_User] = self.user_repo.get_by_pk(pk=user_id)
        logger.info(f"Get Profile By User ID > User: {user}")
        self.profile_repo.get_profile_by_user_id(user_id=user_id)
        return None
