import json

from typing import Optional

from django.http import HttpResponse

from apps.core.models import Source, State
from apps.dictionary.enums import (
    Type as DictionaryType,
    Subtype as DictionarySubtype,
    Origin as DictionaryOrigin,
    State as DictionaryState,
)

from apps.dictionary.models import (
    Word,
    Pronunciation,
    Definition,
    Example,
)


# Create your views here.
def get_source(
    type: DictionaryType = DictionaryType.DEFAULT,
    subtype: DictionarySubtype = DictionarySubtype.DEFAULT,
    origin: DictionaryOrigin = DictionaryOrigin.DEFAULT,
    source: Optional[str] = None,
) -> Source:
    return Source.objects.filter(type=type.value, subtype=subtype.value, origin=origin.value, source=source).first()


def dictionary_details(request):
    source = get_source(
        type=DictionaryType.WORD,
        subtype=DictionarySubtype.DEFAULT,
        origin=DictionaryOrigin.WORDNIK_DOT_COM,
    )
    synced_words = State.objects.filter(source=source, state=DictionaryState.SYNCED.value).count()
    words = Word.objects.count()
    pronunciations = Pronunciation.objects.count()
    definitions = Definition.objects.count()
    examples = Example.objects.count()
    data = {
        "synced_words": synced_words,
        "words": words,
        "pronunciations": pronunciations,
        "definitions": definitions,
        "examples": examples,
    }
    return HttpResponse(json.dumps(data, sort_keys=False, indent=4))
