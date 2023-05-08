import json

from django.http import Http404
from django.utils import dateparse

from loguru import logger
from rest_framework import viewsets
from rest_framework.response import Response

from libretranslatepy import LibreTranslateAPI

from apps.core.models import (
    Source,
    Store,
    Language,
)
from apps.data.views import store_in_lake
from apps.dictionary.models import (
    PartOfSpeech,
    Pronunciation,
    Word,
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
from apps.dictionary.enums import (
    Type,
    Subtype,
    State,
    Source as Source_Enum
)

from apps.dictionary.libs import WordnikService


# Create your views here.

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = "word"

    limit_per = 10
    limit_audio = 50  # max 50
    limit_pronunciation = 500  # max 500
    limit_definition = 500  # max 500
    limit_example = 50  # max 50
    limit_relation = 1000  # max 1000

    delay = 100 * 24 * 60 * 60  # 100 days
    delay_audio = 6 * 60 * 60  # 6 hours

    limit_enabled = False
    translation_enabled = True

    wordnik = WordnikService()
    translator = LibreTranslateAPI('https://translate.argosopentech.com/')

    def retrieve(self, request, *args, **kwargs):
        try:
            word = self.get_object()
            if word and word.word != kwargs.get("word"):
                raise Http404(f"Not matched")
            word = self.get_remote_word(request, kwargs, word_ref=word)
        except Http404:
            logger.exception("What?!")
            word = self.get_remote_word(request, kwargs)

        if not word:
            word = kwargs.get('word')
            raise Http404(f"Word {word} does not exist")

        serializer = self.get_serializer(word)
        data = serializer.data

        return Response(data)

    def is_expired(self, ref, type, subtype, extra, delay) -> bool:
        try:
            store = Store.objects.get(ref=ref, type=type, subtype=subtype, extra=extra)
            return store.is_expired(delay)
        except Store.DoesNotExist:
            logger.exception('What?!')
            return True

    def store_expire(self, ref, type, subtype, extra):
        store, created = Store.objects.update_or_create(
            ref=ref,
            type=type,
            subtype=subtype,
            extra=extra,
            defaults={
                'state': State.SYNCED.name
            }
        )
        logger.debug(f'{store} [created : {created}]')

    def store_synced(self, ref, type, subtype):
        store, created = Store.objects.update_or_create(
            ref=ref,
            type=type,
            subtype=subtype,
            defaults={
                'state': State.SYNCED.name
            }
        )
        logger.debug(f'{store} [created : {created}]')

    def get_remote_word(self, request, kwargs, word_ref=None):
        source = request.GET.get('source')
        target = request.GET.get('target')
        word = kwargs.get('word')
        word = word.lower()

        logger.debug(f'calling remote word [source: {source}, target: {target}, word: {word}]')
        return self.get_word_by_wordnik(source, target, word, word_ref)

    def get_word_by_wordnik(self, source, target, word, word_ref):

        pronunciations = None
        audios = None
        definitions = None
        examples = None
        relations = None

        # for first time check that it has at least definitions
        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.name,
            Subtype.DEFINITION.name,
            None,
            self.delay
        ):
            logger.debug(f'wordnik.get_definitions')
            definitions = self.wordnik.get_definitions(word, limit=self.limit_definition)

        if not definitions:
            return word_ref

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.name,
            Subtype.PRONUNCIATION.name,
            None,
            self.delay
        ):
            logger.debug(f'wordnik.get_pronunciations')
            pronunciations = self.wordnik.get_pronunciations(word, limit=self.limit_pronunciation)

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.name,
            Subtype.AUDIO.name,
            None,
            self.delay
        ):
            logger.debug(f'wordnik.get_audios')
            audios = self.wordnik.get_audios(word, limit=self.limit_audio)

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.name,
            Subtype.EXAMPLE.name,
            None,
            self.delay
        ):
            logger.debug(f'wordnik.get_examples')
            examples = self.wordnik.get_examples(word, limit=self.limit_example)

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.name,
            Subtype.RELATION.name,
            None,
            self.delay
        ):
            logger.debug(f'wordnik.get_relations')
            relations = self.wordnik.get_relations(word, limit=self.limit_relation)

        if (
            (not word_ref and definitions)
            or
            (
                word_ref and self.is_expired(
                word_ref.id,
                Type.WORD.name,
                Subtype.DEFAULT.name,
                None,
                self.delay)
            )
        ):
            logger.debug(f"wordnik.get_relations")
            language = self.get_or_create_language()
            word_ref = self.get_or_create_word(language, word)
            self.store_expire(word_ref.id, Type.WORD.name, Subtype.DEFAULT.name, None)

            if self.translation_enabled:
                if source and target and source != target and source == "en" and self.is_expired(
                    word_ref.id,
                    Type.WORD.name,
                    Subtype.TRANSLATION.name,
                    source + target,
                    self.delay
                ):
                    logger.debug("producing translations")
                    if not self.has_language(code=source) or not self.has_language(code=target):
                        for language in self.translator.languages():
                            logger.debug("storing languages")
                            self.get_or_create_language(language["code"], language["name"])

                    source = self.get_language(source)
                    target = self.get_language(target)

                    logger.debug(f"Source {source.code}, Target {target.code}")

                    if source and target:
                        try:
                            translation = self.translator.translate(word, source.code, target.code)
                            logger.debug(f"Translation of {word} is {translation}")
                            if translation:
                                store_in_lake(
                                    source=Source_Enum.LIBRE_TRANSLATE.name,
                                    ref=dict(
                                        word=word,
                                        source=source.code,
                                        target=target.code,
                                        type=Type.WORD.name,
                                        subtype=Subtype.TRANSLATION.name,
                                    ),
                                    raw=translation
                                )
                                translation = self.get_or_create_word(target, translation)
                                self.build_or_create_translation(source, target, word_ref, translation)
                                self.store_expire(word_ref.id, Type.WORD.name, Subtype.TRANSLATION.name,
                                                  source.code + target.code)
                        except Http404:
                            logger.exception('What?!')

            if pronunciations:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.name,
                    ref=dict(
                        word=word,
                        type=Type.WORD.name,
                        subtype=Subtype.PRONUNCIATION.name,
                    ),
                    raw=pronunciations
                )
                self.build_or_create_pronunciations(word_ref, pronunciations)
                self.store_expire(word_ref.id, Type.WORD.name, Subtype.PRONUNCIATION.name, None)

            if audios:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.name,
                    ref=dict(
                        word=word,
                        type=Type.WORD.name,
                        subtype=Subtype.AUDIO.name,
                    ),
                    raw=audios
                )
                self.build_or_create_audios(word_ref, audios)
                self.store_expire(word_ref.id, Type.WORD.name, Subtype.AUDIO.name, None)

            if definitions:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.name,
                    ref=dict(
                        word=word,
                        type=Type.WORD.name,
                        subtype=Subtype.DEFINITION.name,
                    ),
                    raw=definitions
                )
                self.build_or_create_definitions(word_ref, definitions)
                self.store_expire(word_ref.id, Type.WORD.name, Subtype.DEFINITION.name, None)

            if examples:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.name,
                    ref=dict(
                        word=word,
                        type=Type.WORD.name,
                        subtype=Subtype.EXAMPLE.name,
                    ),
                    raw=examples
                )
                self.build_or_create_examples(word_ref, examples=examples.examples)
                self.store_expire(word_ref.id, Type.WORD.name, Subtype.EXAMPLE.name, None)

            if relations:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.name,
                    ref=dict(
                        word=word,
                        type=Type.WORD.name,
                        subtype=Subtype.RELATION.name,
                    ),
                    raw=relations
                )
                self.build_or_create_relations(word_ref, relations)
                self.store_expire(word_ref.id, Type.WORD.name, Subtype.RELATION.name, None)

        return word_ref

    def get_or_create_source(
        self,
        type=Type.DEFAULT.name,
        subtype=Subtype.DEFAULT.name,
        source='default'
    ):
        source, created = Source.objects.get_or_create(
            type=type,
            subtype=subtype,
            source=source
        )
        logger.debug(f'{source} [created : {created}]')
        return source

    def has_language(self, code=None, name=None):
        try:
            Language.objects.get(code=code, name=name)
            return True
        except Language.DoesNotExist:
            return False

    def get_or_create_language(self, code='en', name='English'):
        source = self.get_or_create_source(type=Type.DICTIONARY.name)
        language, created = Language.objects.get_or_create(
            source=source,
            code=code,
            name=name
        )
        logger.debug(f'{language} [created : {created}]')
        return language

    def get_language(self, code):
        try:
            return Language.objects.get(code=code)
        except Language.DoesNotExist:
            return None

    def get_or_create_part_of_speech(self, part_of_speech):
        part_of_speech, created = PartOfSpeech.objects.get_or_create(part_of_speech=part_of_speech)
        logger.debug(f'{part_of_speech} [created : {created}]')
        return part_of_speech

    def get_or_create_relation_type(self, relation_type):
        relation_type, created = RelationType.objects.get_or_create(relation_type=relation_type)
        logger.debug(f'{relation_type} [created : {created}]')
        return relation_type

    def get_or_create_word(self, language, word):
        word, created = Word.objects.get_or_create(language=language, word=word)
        logger.debug(f'{word} [created : {created}]')
        return word

    def build_or_create_translation(self, source, target, word, translation):
        if not translation:
            return

        translation, created = Translation.objects.get_or_create(
            source=source,
            target=target,
            source_word=word,
            target_word=translation,
        )
        logger.debug(f'{translation} [created : {created}]')

    def build_or_create_pronunciations(self, word, pronunciations):
        logger.debug(f'[word: {word}][pronunciations: {len(pronunciations)}]')
        pers = {}
        for pronunciation in pronunciations:
            source = pronunciation.rawType
            if source not in pers:
                pers[source] = 0
            if self.limit_enabled and pers[source] >= self.limit_per:
                continue
            self.build_or_create_pronunciation(word, pronunciation)
            pers[source] = pers[source] + 1

    def build_or_create_pronunciation(self, word, pronunciation):
        source = self.get_or_create_source(
            type=Type.DICTIONARY.name,
            subtype=Subtype.WORD.name,
            source=pronunciation.rawType
        )
        logger.debug(f'Pronunciation.objects.get_or_create {source.source} {word.word} {pronunciation.raw}')

        pronunciation, created = Pronunciation.objects.get_or_create(
            source=source,
            word=word,
            pronunciation=pronunciation.raw
        )
        logger.debug(f'{pronunciation} [created : {created}]')

    def build_or_create_audios(self, word, audios):
        pers = {}
        for audio in audios:
            source = audio.createdBy
            if source not in pers:
                pers[source] = 0
            if self.limit_enabled and pers[source] >= self.limit_per:
                continue
            self.build_or_create_audio(word, audio)
            pers[source] = pers[source] + 1

    def build_or_create_audio(self, word, audio):
        if not audio.createdBy:
            return
        source = self.get_or_create_source(type=Type.DICTIONARY.name, subtype=Subtype.WORD.name,
                                           source=audio.createdBy)
        pronunciation, created = Pronunciation.objects.update_or_create(
            source=source,
            word=word,
            defaults={
                'url': audio.fileUrl
            }
        )
        logger.debug(f'{pronunciation} [created : {created}]')

    def build_or_create_definitions(self, word, definitions):
        pers = {}
        for definition in definitions:
            if None in [definition.sourceDictionary, definition.partOfSpeech, definition.text]:
                continue
            source = definition.sourceDictionary
            if source not in pers:
                pers[source] = 0
            if self.limit_enabled and pers[source] >= self.limit_per:
                continue
            self.build_or_create_definition(word, definition)
            pers[source] = pers[source] + 1

    def build_or_create_definition(self, word, definition):
        examples = definition.exampleUses
        source = self.get_or_create_source(type=Type.DICTIONARY.name, subtype=Subtype.WORD.name,
                                           source=definition.sourceDictionary)
        part_of_speech = self.get_or_create_part_of_speech(definition.partOfSpeech)
        definition, created = Definition.objects.get_or_create(
            source=source,
            part_of_speech=part_of_speech,
            word=word,
            definition=definition.text
        )
        logger.debug(f'{definition} [created : {created}]')
        self.build_or_create_examples(word, definition, examples)

    def build_or_create_examples(self, word, definition=None, examples=None):
        for example in examples:
            self.build_or_create_example(word, definition, example)

    def build_or_create_example(self, word, definition=None, example=None):
        if definition:
            example, created = Example.objects.get_or_create(
                word=word,
                definition=definition,
                example=example.text
            )
        else:
            year = f'{example.year}-01-01' if isinstance(example.year, int) else example.year
            example, created = Example.objects.update_or_create(
                word=word,
                example=example.text,
                defaults={
                    'author': example.author if hasattr(example, 'author') else None,
                    'title': example.title,
                    'url': example.url,
                    'year': dateparse.parse_date(year) if year else None
                }
            )
        logger.debug(f'{example} [created : {created}]')

    def build_or_create_relations(self, word, relations):
        for relation in relations:
            self.build_or_create_relation(word, relation)

    def build_or_create_relation(self, word, relation):
        if None in [relation.relationshipType, relation.words]:
            return

        pers = {}
        type = relation.relationshipType

        language = self.get_or_create_language()
        relation_type = self.get_or_create_relation_type(type)

        for relation_word in relation.words:
            if type not in pers:
                pers[type] = 0
            if self.limit_enabled and pers[type] >= self.limit_per:
                continue
            pers[type] = pers[type] + 1

            relation_word = relation_word.lower()
            relation_word = self.get_or_create_word(language, relation_word)

            left_word = word if word.id <= relation_word.id else relation_word
            right_word = relation_word if word.id <= relation_word.id else word

            relation, created = Relation.objects.get_or_create(
                relation_type=relation_type,
                left_word=left_word,
                right_word=right_word
            )
            logger.debug(f'{relation} [created : {created}]')


class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
