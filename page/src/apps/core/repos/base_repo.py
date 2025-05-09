import uuid
from abc import ABC
from typing import Any, Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

_T = TypeVar("_T", bound=Model)


class BaseRepo(ABC, Generic[_T]):
    model: type[_T]

    def __init__(self, model: type[_T]):
        self.model = model

    def get_by_pk(self, pk: str | uuid.UUID) -> _T | None:
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get_all(self) -> list[_T]:
        return list(self.model.objects.all())

    def exists(self, **kwargs: Any) -> bool:
        return self.model.objects.filter(**kwargs).exists()

    def filter(self, **kwargs: Any) -> list[_T]:
        return list(self.model.objects.filter(**kwargs))

    def create(self, **kwargs: Any) -> _T:
        return self.model.objects.create(**kwargs)

    def update(self, instance: _T, **kwargs: Any) -> _T:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return None

    def update_by_pk(self, pk: str | uuid.UUID, **kwargs: Any) -> _T | None:
        instance = self.get_by_pk(pk)
        return self.update(instance, **kwargs) if instance else None

    def delete(self, instance: _T) -> None:
        instance.delete()

    def delete_by_id(self, pk: str | uuid.UUID) -> bool:
        instance = self.get_by_pk(pk)
        if instance:
            instance.delete()
            return True
        return False
