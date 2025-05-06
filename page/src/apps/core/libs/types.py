from enum import Enum
from typing import TypeVar

_BE = TypeVar("_BE", bound="_BaseEnum")


class _BaseEnum(Enum):
    pass
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


class StrBaseEnum(str, _BaseEnum):
    pass


class IntBaseEnum(str, _BaseEnum):
    pass
