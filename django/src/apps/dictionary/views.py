from django.http import Http404

from loguru import logger
from rest_framework import viewsets
from rest_framework.response import Response

from apps.dictionary.models import (
    PartOfSpeech,
    Pronunciation,
    Word,
    Attribution,
    Definition,
    Example,
    RelationType,
    Relation,
    Translation,
)
from apps.dictionary.serializers import (
    WordSerializer,
    DefinitionSerializer,
)

from .services import WordService


# Create your views here.


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = "word"

    def retrieve(self, request, *args, **kwargs):
        try:
            ref = self.get_object()
            if ref and ref.word != kwargs.get("word"):
                raise Http404(f"Not matched")
            ref = self.get_remote_word(request, kwargs, ref=ref)
        except Http404:
            ref = self.get_remote_word(request, kwargs)

        if not ref:
            word = kwargs.get("word")
            raise Http404(f"Word {word} does not exist")

        serializer = self.get_serializer(ref)
        data = serializer.data
        return Response(data)

    def get_remote_word(self, request, kwargs, ref=None):
        source = request.GET.get("source")
        target = request.GET.get("target")
        word = kwargs.get("word")
        word = word.lower()

        if ref:
            logger.debug(f"OLD: {ref} word [source: {source}, target: {target}")
        else:
            logger.debug(f"NEW: {word} [source: {source}, target: {target}")

        # using wordnik
        return self.get_word_by_wordnik(source=source, target=target, ref=ref, word=word)

    def get_word_by_wordnik(self, source, target, ref, word):
        service = WordService(ref=ref, word=word)
        return service.get_or_update_word(source_language_code=source, target_language_code=target)


class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
