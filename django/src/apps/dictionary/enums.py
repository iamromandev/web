import enum


class Type(enum.Enum):
    DEFAULT = "DEFAULT"
    WORD = "WORD"
    DEFINITION = "DEFINITION"

    def is_equal(self, value: str) -> bool:
        return value == self.value


class Subtype(enum.Enum):
    DEFAULT = "DEFAULT"
    PRONUNCIATION = "PRONUNCIATION"
    AUDIO = "AUDIO"
    DEFINITION = "DEFINITION"
    PART_OF_SPEECH = "PART_OF_SPEECH"
    ATTRIBUTION = "ATTRIBUTION"
    EXAMPLE = "EXAMPLE"
    RELATION = "RELATION"
    TRANSLATION = "TRANSLATION"

    def is_equal(self, value: str) -> bool:
        return value == self.value


class Origin(enum.Enum):
    DEFAULT = "DEFAULT"
    WORDNIK_DOT_COM = "WORDNIK_DOT_COM"
    LIBRE_TRANSLATE_DOT_COM = "LIBRE_TRANSLATE_DOT_COM"


class State(enum.Enum):
    DEFAULT = "DEFAULT"
    SYNCED = "SYNCED"
    NOT_FOUND = "NOT_FOUND"
