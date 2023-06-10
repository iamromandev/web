from uuid import UUID
from typing import Optional

from loguru import logger

from .models import (
    Source,
    Language,
    State,
)


class LanguageService:
    def has_language(self, source: Source, code=None, name=None):
        try:
            if code:
                if name:
                    Language.objects.get(source=source, code=code, name=name)
                    return True
                else:
                    Language.objects.get(source=source, code=code)
                    return True
            return False
        except Language.DoesNotExist as error:
            logger.error(error)
            return False

    def get_or_create_language(self, source: Source, code="en", name="English"):
        language, created = Language.objects.get_or_create(source=source, code=code, name=name)
        if created:
            logger.debug(f"{language} [created : {created}]")
        return language

    def get_language(self, source: Source, code):
        try:
            return Language.objects.get(source=source, code=code)
        except Language.DoesNotExist:
            return None


class StateService:
    def update_state(self, ref: UUID, source: Source, state: str, extra: Optional[str] = None):
        state, created = State.objects.get_or_create(ref=ref, source=source, defaults={"state": state, "extra": extra})
        if created:
            logger.debug(f"{state} [created : {created}]")
