from django.http import Http404
from django.utils import dateparse

from loguru import logger
from rest_framework import viewsets
from rest_framework.response import Response

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
from apps.dictionary.enums import (
    Type,
    Subtype,
    State,
    Source as Source_Enum
)

from apps.dictionary.libs import WordnikService
from apps.dictionary.libs import TranslationService


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
    translator = TranslationService()

    def retrieve(self, request, *args, **kwargs):
        try:
            word = self.get_object()
            if word and word.word != kwargs.get("word"):
                raise Http404(f"Not matched")
            word = self.get_remote_word(request, kwargs, word_ref=word)
        except Http404:
            word = self.get_remote_word(request, kwargs)

        if not word:
            word = kwargs.get("word")
            raise Http404(f"Word {word} does not exist")

        serializer = self.get_serializer(word)
        data = serializer.data

        return Response(data)

    def is_expired(self, ref, type, subtype, extra, delay) -> bool:
        try:
            store = Store.objects.get(ref=ref, type=type, subtype=subtype, extra=extra)
            return store.is_expired(delay)
        except Store.DoesNotExist:
            return True

    def store_expire(self, ref, type, subtype, extra):
        store, created = Store.objects.update_or_create(
            ref=ref,
            type=type,
            subtype=subtype,
            extra=extra,
            defaults={
                "state": State.SYNCED.value
            }
        )
        # logger.debug(f"{store} [created : {created}]")

    def store_synced(self, ref, type, subtype):
        store, created = Store.objects.update_or_create(
            ref=ref,
            type=type,
            subtype=subtype,
            defaults={
                "state": State.SYNCED.value
            }
        )
        # logger.debug(f"{store} [created : {created}]")

    def get_remote_word(self, request, kwargs, word_ref=None):
        source = request.GET.get("source")
        target = request.GET.get("target")
        word = kwargs.get("word")
        word = word.lower()

        logger.debug(f'calling remote word [source: {source}, target: {target}, word: {word}]')
        return self.get_word_by_wordnik(source, target, word, word_ref)

    def get_word_by_wordnik(self, source, target, word, word_ref):

        error_pronunciations, pronunciations = True, None
        error_audios, audios = True, None
        error_definitions, definitions = True, None
        error_examples, examples = True, None
        error_relations, relations = True, None

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.PRONUNCIATION.value,
            None,
            self.delay
        ):
            error_pronunciations, pronunciations = self.wordnik.get_pronunciations(word, limit=self.limit_pronunciation)
            if error_pronunciations:
                logger.error(f"api limit on wordnik.get_pronunciations")
                return word_ref
            logger.debug(f'wordnik.get_pronunciations: {len(pronunciations if pronunciations else [])}')

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.AUDIO.value,
            None,
            self.delay
        ):
            error_audios, audios = self.wordnik.get_audios(word, limit=self.limit_audio)
            if error_audios:
                logger.error(f'api limit on wordnik.get_audios')
                return word_ref
            logger.debug(f'wordnik.get_audios: {len(audios if audios else [])}')

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.DEFINITION.value,
            None,
            self.delay
        ):
            error_definitions, definitions = self.wordnik.get_definitions(word, limit=self.limit_definition)
            if error_definitions:
                logger.error(f'api limit on wordnik.get_definitions')
                return word_ref
            logger.debug(f"wordnik.get_definitions: {len(definitions if definitions else [])}")

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.EXAMPLE.value,
            None,
            self.delay
        ):
            error_examples, examples = self.wordnik.get_examples(word, limit=self.limit_example)
            if error_examples:
                logger.error(f"api limit on wordnik.get_examples")
                return word_ref
            logger.debug(f"wordnik.get_examples: {len(examples.examples) if hasattr(examples, 'examples') else 0}")

        if not word_ref or self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.RELATION.value,
            None,
            self.delay
        ):
            error_relations, relations = self.wordnik.get_relations(word, limit=self.limit_relation)
            if error_relations:
                logger.error(f"api limit on wordnik.get_relations")
                return word_ref
            logger.debug(f"wordnik.get_relations: {len(relations) if relations else 0}")

        has_resources = not (
            error_pronunciations and error_audios and error_definitions and error_examples and error_relations)
        if (
            (
                not word_ref and has_resources
            )
            or
            (
                word_ref and self.is_expired(
                word_ref.id,
                Type.WORD.value,
                Subtype.DEFAULT.value,
                None,
                self.delay
            )
            )
        ):
            language = self.get_or_create_language(code="en", name="English")
            word_ref = self.get_or_create_word(language, word)
            self.store_expire(word_ref.id, Type.WORD.value, Subtype.DEFAULT.value, None)

            if self.translation_enabled:
                self.do_translation_job(source, target, word, word_ref)

            if not error_pronunciations and pronunciations:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.value,
                    ref=dict(
                        word=word,
                        type=Type.WORD.value,
                        subtype=Subtype.PRONUNCIATION.value,
                    ),
                    raw=pronunciations
                )
                self.build_or_create_pronunciations(word_ref, pronunciations)
                self.store_expire(word_ref.id, Type.WORD.value, Subtype.PRONUNCIATION.value, None)

            if not error_audios and audios:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.value,
                    ref=dict(
                        word=word,
                        type=Type.WORD.value,
                        subtype=Subtype.AUDIO.value,
                    ),
                    raw=audios
                )
                self.build_or_create_audios(word_ref, audios)
                self.store_expire(word_ref.id, Type.WORD.value, Subtype.AUDIO.value, None)

            if not error_definitions and definitions:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.value,
                    ref=dict(
                        word=word,
                        type=Type.WORD.value,
                        subtype=Subtype.DEFINITION.value,
                    ),
                    raw=definitions
                )
                self.build_or_create_definitions(word_ref, definitions)
                self.store_expire(word_ref.id, Type.WORD.value, Subtype.DEFINITION.value, None)

            if not error_examples and examples:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.value,
                    ref=dict(
                        word=word,
                        type=Type.WORD.value,
                        subtype=Subtype.EXAMPLE.value,
                    ),
                    raw=examples
                )
                self.build_or_create_examples(word_ref, examples=examples.examples)
                self.store_expire(word_ref.id, Type.WORD.value, Subtype.EXAMPLE.value, None)

            if not error_relations and relations:
                # store in data lake
                store_in_lake(
                    source=Source_Enum.WORDNIK.value,
                    ref=dict(
                        word=word,
                        type=Type.WORD.value,
                        subtype=Subtype.RELATION.value,
                    ),
                    raw=relations
                )
                self.build_or_create_relations(word_ref, relations)
                self.store_expire(word_ref.id, Type.WORD.value, Subtype.RELATION.value, None)

            logger.debug(f"Completed {word_ref.word}")

        return word_ref

    def get_or_create_source(
        self,
        type=Type.DEFAULT.value,
        subtype=Subtype.DEFAULT.value,
        source=Source_Enum.DEFAULT.value,
    ):
        source, created = Source.objects.get_or_create(
            type=type,
            subtype=subtype,
            source=source
        )
        if created:
            logger.debug(f'{source} [created : {created}]')
        return source

    def has_language(self, code=None, name=None):
        try:
            if code:
                if name:
                    Language.objects.get(code=code, name=name)
                    return True
                else:
                    Language.objects.get(code=code)
                    return True
            return False
        except Language.DoesNotExist as error:
            logger.error(error)
            return False

    def get_or_create_language(self, code='en', name='English'):
        source = self.get_or_create_source(type=Type.DICTIONARY.value)
        language, created = Language.objects.get_or_create(
            source=source,
            code=code,
            name=name
        )
        if created:
            logger.debug(f'{language} [created : {created}]')
        return language

    def get_language(self, code):
        try:
            return Language.objects.get(code=code)
        except Language.DoesNotExist:
            return None

    def get_or_create_part_of_speech(self, part_of_speech):
        part_of_speech, created = PartOfSpeech.objects.get_or_create(part_of_speech=part_of_speech)
        if created:
            logger.debug(f'{part_of_speech} [created : {created}]')
        return part_of_speech

    def get_or_create_attribution(self, url, text):
        if url or text:
            attribution, created = Attribution.objects.get_or_create(
                url=url,
                text=text,
            )
            if created:
                logger.debug(f'Attribution: {attribution.url} [created : {created}]')
            return attribution
        return None

    def get_or_create_relation_type(self, relation_type):
        relation_type, created = RelationType.objects.get_or_create(relation_type=relation_type)
        if created:
            logger.debug(f'{relation_type} [created : {created}]')
        return relation_type

    def get_or_create_word(self, language, word):
        word, created = Word.objects.get_or_create(language=language, word=word)
        if created:
            logger.debug(f'{word} [created : {created}]')
        return word

    def do_translation_job(self, source, target, word, word_ref):
        if source and target and source != target and source == 'en' and self.is_expired(
            word_ref.id,
            Type.WORD.value,
            Subtype.TRANSLATION.value,
            source + target,
            self.delay
        ):
            logger.debug('producing translations')
            if not (self.has_language(code=source) and self.has_language(code=target)):
                logger.debug('storing languages for translations support')
                error_languages, languages = self.translator.languages()

                if not error_languages and languages:
                    for language in languages:
                        self.get_or_create_language(language['code'], language['name'])

            source = self.get_language(source)
            target = self.get_language(target)

            logger.debug(f'word {word} source {source.code}, target {target.code}')

            if source and target:
                try:
                    error_translation, translation = self.translator.translate(word, source.code, target.code)
                    logger.debug(f'translation: {translation}')
                    if not error_translation and translation:
                        store_in_lake(
                            source=Source_Enum.LIBRE_TRANSLATE.value,
                            ref=dict(
                                word=word,
                                source=source.code,
                                target=target.code,
                                type=Type.WORD.value,
                                subtype=Subtype.TRANSLATION.value,
                            ),
                            raw=translation
                        )
                        translation = self.get_or_create_word(target, translation)
                        self.build_or_create_translation(source, target, word_ref, translation)
                        self.store_expire(
                            word_ref.id,
                            Type.WORD.value,
                            Subtype.TRANSLATION.value,
                            source.code + target.code
                        )
                except Http404 as error:
                    logger.error(error)

    def build_or_create_translation(self, source, target, word, translation):
        if not translation:
            return

        translation, created = Translation.objects.get_or_create(
            source=source,
            target=target,
            source_word=word,
            target_word=translation,
        )
        if created:
            logger.debug(f'{translation} [created : {created}]')

    def build_or_create_pronunciations(self, word, pronunciations):
        logger.debug(f"[word: {word}][pronunciations: {len(pronunciations)}]")
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
            type=Type.DICTIONARY.value,
            subtype=Subtype.WORD.value,
            source=pronunciation.rawType
        )
        logger.debug(f"Pronunciation.objects.get_or_create {source.source} {word.word} {pronunciation.raw}")

        pronunciation, created = Pronunciation.objects.get_or_create(
            source=source,
            word=word,
            pronunciation=pronunciation.raw
        )
        if created:
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
        source = self.get_or_create_source(type=Type.DICTIONARY.value, subtype=Subtype.WORD.value,
                                           source=audio.createdBy)
        pronunciation, created = Pronunciation.objects.update_or_create(
            source=source,
            word=word,
            defaults={
                'url': audio.fileUrl
            }
        )
        if created:
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
        # logger.debug(f'created definitions for {word.word}')

    def build_or_create_definition(self, word, definition):
        examples = definition.exampleUses
        source = self.get_or_create_source(
            type=Type.DICTIONARY.value,
            subtype=Subtype.WORD.value,
            source=definition.sourceDictionary
        )
        part_of_speech = self.get_or_create_part_of_speech(definition.partOfSpeech)
        attribution = self.get_or_create_attribution(definition.attributionUrl, definition.attributionText)
        definition, created = Definition.objects.get_or_create(
            source=source,
            part_of_speech=part_of_speech,
            attribution=attribution,
            word=word,
            definition=definition.text
        )
        if created:
            logger.debug(f'{definition} [created : {created}]')
        self.build_or_create_examples(word, definition, examples)

    def build_or_create_examples(self, word, definition=None, examples=None):
        for example in examples:
            self.build_or_create_example(word, definition, example)
        # logger.debug(f'created examples for {word.word}')

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
                    "author": example.author if hasattr(example, "author") else None,
                    "title": example.title,
                    "url": example.url,
                    "year": dateparse.parse_date(year) if year else None
                }
            )
        if created:
            logger.debug(f'{example} [created : {created}]')

    def build_or_create_relations(self, word, relations):
        for relation in relations:
            self.build_or_create_relation(word, relation)
        logger.debug(f'created relations for {word.word}')

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
            # logger.debug(f'{relation} [created : {created}]')


class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
