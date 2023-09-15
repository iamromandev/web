import enum


class Type(enum.Enum):
    DEFAULT = "DEFAULT"
    TODO = "TODO"

    def is_equal(self, value: str) -> bool:
        return value == self.value


class Subtype(enum.Enum):
    DEFAULT = "DEFAULT"

    def is_equal(self, value: str) -> bool:
        return value == self.value


class Origin(enum.Enum):
    DEFAULT = "DEFAULT"
