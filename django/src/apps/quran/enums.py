import enum


class Source(enum.Enum):
    DEFAULT = "DEFAULT"
    QURAN_DOT_COM = "QURAN_DOT_COM"


class Type(enum.Enum):
    DEFAULT = "DEFAULT"
    QURAN = "QURAN"
    SURAH = "SURAH"
    AYAH = "AYAH"


class Subtype(enum.Enum):
    DEFAULT = "DEFAULT"
    SURAH = "SURAH"
    AYAH = "AYAH"
