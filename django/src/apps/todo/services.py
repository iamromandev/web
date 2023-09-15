from typing import Optional

from loguru import logger

from apps.core.models import (
    Source,
    Language,
)
from apps.core.services import (
    LanguageService,
)

from .enums import (
    Type,
    Subtype,
    Origin,
)
from .models import (
    Todo,
)


class TodoService:
    def __init__(self):
        self.language_service = LanguageService()

    def get_or_create_source(
        self,
        type: Type = Type.DEFAULT,
        subtype: Subtype = Subtype.DEFAULT,
        origin: Origin = Origin.DEFAULT,
        source: Optional[str] = None,
    ) -> Source:
        source, created = Source.objects.get_or_create(
            type=type.value, subtype=subtype.value, origin=origin.value, source=source
        )
        if created:
            logger.debug(f"{source} [created : {created}]")
        return source

    def get_or_create_todo(self, title: str) -> Todo:
        source = self.get_or_create_source()
        language = self.language_service.get_or_create_language(source=source)

        todo, created = Todo.objects.get_or_create(source=source, language=language, title=title)
        if created:
            logger.debug(f"{todo} [created : {created}]")
        return todo
