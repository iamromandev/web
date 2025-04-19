from abc import ABC
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

_T = TypeVar("_T", bound=Model)


class BaseRepo(ABC, Generic[_T]):
    model: type[_T]

    def __init__(self, model: type[_T]):
        self.model = model

    def get_all(self) -> list[_T]:
        return list(self.model.objects.all())

    def get_by_id(self, id: UUID) -> Optional[_T]:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs: Any) -> _T:
        return self.model.objects.create(**kwargs)


    def update(self, id: UUID, **kwargs: Any) -> Optional[_T]:
        instance = self.get_by_id(id)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        return None

    def delete(self, instance: _T) -> None:
        instance.delete()

    def delete_by_id(self, id: UUID) -> bool:
        instance = self.get_by_id(id)
        if instance:
            instance.delete()
            return True
        return False
