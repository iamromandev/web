import enum


class Type(enum.Enum):
    DEFAULT = "DEFAULT"
    DICTIONARY = "DICTIONARY"
    WORD = "WORD"


class Subtype(enum.Enum):
    DEFAULT = "DEFAULT"
    WORD = "WORD"
    PRONUNCIATION = "PRONUNCIATION"
    AUDIO = "AUDIO"
    DEFINITION = "DEFINITION"
    EXAMPLE = "EXAMPLE"
    RELATION = "RELATION"
    TRANSLATION = "TRANSLATION"


class State(enum.Enum):
    DEFAULT = "DEFAULT"
    SYNCED = "SYNCED"


class Source(enum.Enum):
    DEFAULT = "DEFAULT"
    WORDNIK = "WORDNIK"
    LIBRE_TRANSLATE = "LIBRE_TRANSLATE"
