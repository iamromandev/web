import json

from django.http import HttpResponse

from apps.core.models import State
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


def dictionary_details(request):
    synced_words = State.objects.filter(
        type=DictionaryType.WORD.value, subtype=DictionarySubtype.DEFAULT.value, state=State.SYNCED.value
    ).count()
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
