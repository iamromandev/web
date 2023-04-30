import enum


class Type(enum.Enum):
    DEFAULT = 'default'
    DICTIONARY = 'dictionary'
    WORD = 'word'


class Subtype(enum.Enum):
    DEFAULT = 'default'
    WORD = 'word'
    PRONUNCIATION = 'pronunciation'
    AUDIO = 'audio'
    DEFINITION = 'definition'
    EXAMPLE = 'example'
    RELATION = 'relation'
    TRANSLATION = 'translation'


class State(enum.Enum):
    DEFAULT = 'default'
    SYNCED = 'synced'
