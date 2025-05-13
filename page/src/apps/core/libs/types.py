from enum import Enum
from typing import Generic, TypeVar

_T = TypeVar("_T")


class BaseEnum(Enum, Generic[_T]):
    def __init__(self, value: _T) -> None:
        self._value_ = value

    @property
    def value(self) -> _T:
        return self._value_

    @classmethod
    def from_value(cls, value: _T) -> "BaseEnum[_T]":
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")
    # @classmethod
    # def choices(cls: Type[_BaseEnum]) -> list[tuple[str, T]]:
    #     return [(member.name, member.value) for member in cls]
    #
    # @classmethod
    # def get_value(cls, name: str) -> Optional[T]:
    #     try:
    #         return cls[name].value
    #     except KeyError:
    #         return None
    #
    # @classmethod
    # def get_name(cls, value: T) -> Optional[str]:
    #     for member in cls:
    #         if member.value == value:
    #             return member.name
    #     return None
    #
    # @classmethod
    # def get_display_name(cls, value: T) -> Optional[str]:
    #     for member in cls:
    #         if member.value == value:
    #             return member.name.replace("_", " ").title()
    #     return None
    #
    # @classmethod
    # def has_value(cls, value: T) -> bool:
    #     return any(member.value == value for member in cls)
    #
    # @classmethod
    # def has_name(cls, name: str) -> bool:
    #     return name in cls.__members__


class StrBaseEnum(BaseEnum[str]):
    pass


class IntBaseEnum(BaseEnum[int]):
    pass
