from typing import Optional

from django.utils import dateparse

from loguru import logger

from config.settings import TRANSLATION_ENABLED
from apps.core.models import (
    Source,
    Language,
    State,
)
from apps.core.services import (
    LanguageService,
    StateService,
)
from apps.data.views import store_in_lake

from .enums import (
    Type as DictionaryType,
    Subtype as DictionarySubtype,
    Origin as DictionaryOrigin,
    State as DictionaryState,
)

from .libs import WordnikService, Translator
from .utils import join_list_in_sort

from .models import (
    Word,
    PartOfSpeech,
    Pronunciation,
    Attribution,
    Definition,
    Example,
    RelationType,
    Relation,
    Translation,
)


class Service:
    def __init__(self, ref: Optional[Word], word: str):
        self.ref = ref
        self.word = word
        self.source = None
        self.source_language = None
        self.target_language = None

        self.delay_s = 100 * 24 * 60 * 60  # 100 days
        self.limit_enabled = False
        self.limit_per = 10
        self.translation_enabled = TRANSLATION_ENABLED

        self.error = True
        self.raw = None
        self.result = None

        self.language_service = LanguageService()
        self.state_service = StateService()

        self.wordnik = WordnikService()

    def is_expired(self, extra: Optional[str] = None) -> bool:
        if not self.ref:
            return True
        try:
            state = State.objects.get(ref=self.ref.id, source=self.source, extra=extra)
            return DictionaryState.SYNCED.value == state.state and state.is_expired(self.delay_s)
        except State.DoesNotExist:
            return True

    def get_or_create_source(
        self,
        type: DictionaryType = DictionaryType.DEFAULT,
        subtype: DictionarySubtype = DictionarySubtype.DEFAULT,
        origin: DictionaryOrigin = DictionaryOrigin.DEFAULT,
        source: Optional[str] = None,
    ) -> Source:
        source, created = Source.objects.get_or_create(
            type=type.value, subtype=subtype.value, origin=origin.value, source=source
        )
        if created:
            logger.debug(f"{source} [created : {created}]")
        return source

    def get_or_create_word(self, source: Source, language: Language, word: str) -> Word:
        word, created = Word.objects.get_or_create(source=source, language=language, word=word)
        if created:
            logger.debug(f"{word} [created : {created}]")
        return word

    def get_or_create_part_of_speech(self, part_of_speech):
        source = self.get_or_create_source(
            type=DictionaryType.DEFINITION,
            subtype=DictionarySubtype.PART_OF_SPEECH,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        part_of_speech, created = PartOfSpeech.objects.get_or_create(source=source, part_of_speech=part_of_speech)
        if created:
            logger.debug(f"{part_of_speech} [created : {created}]")
        return part_of_speech

    def get_or_create_attribution(self, url, text):
        if url or text:
            source = self.get_or_create_source(
                type=DictionaryType.DEFINITION,
                subtype=DictionarySubtype.ATTRIBUTION,
                origin=DictionaryOrigin.WORDNIK_DOT_COM,
            )
            attribution, created = Attribution.objects.get_or_create(
                source=source,
                url=url,
                text=text,
            )
            if created:
                logger.debug(f"Attribution: {attribution.url} [created : {created}]")
            return attribution
        return None

    def get_or_create_relation_type(self, source: Source, relation_type):
        relation_type, created = RelationType.objects.get_or_create(source=source, relation_type=relation_type)
        if created:
            logger.debug(f"{relation_type} [created : {created}]")
        return relation_type

    @property
    def has_result(self) -> True:
        return not self.error and self.result

    @property
    def build_state(self) -> DictionaryState:
        if DictionaryType.WORD.is_equal(self.source.type) and DictionarySubtype.DEFAULT.is_equal(self.source.subtype):
            return DictionaryState.SYNCED

        return DictionaryState.SYNCED if self.has_result else DictionaryState.NOT_FOUND

    def update_state(self, extra: Optional[str] = None):
        state = self.build_state
        self.state_service.update_state(ref=self.ref.id, source=self.source, state=state.value, extra=extra)


class WordService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(WordService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.DEFAULT,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.pronunciation_service = PronunciationService(ref=ref, word=word)
        self.audio_service = AudioService(ref=ref, word=word)
        self.definition_service = DefinitionService(ref=ref, word=word)
        self.example_service = ExampleService(ref=ref, word=word)
        self.relation_service = RelationService(ref=ref, word=word)
        if self.translation_enabled:
            self.translation_service = TranslationService(ref=ref, word=word)

    @property
    def services(self) -> tuple:
        return (
            self.pronunciation_service,
            self.audio_service,
            self.definition_service,
            self.example_service,
            self.relation_service,
        )

    @property
    def has_resources(self) -> bool:
        for service in self.services:
            if service.has_result:
                return True
        return False

    def get_or_update_word(self, source_language_code: str, target_language_code: str) -> Optional[Word]:
        for service in self.services:
            service.load()

        if self.has_resources and self.is_expired():
            language = self.language_service.get_or_create_language(source=self.source)
            self.ref = self.get_or_create_word(source=self.source, language=language, word=self.word)
            self.update_state()

            for service in self.services:
                service.ref = self.ref
                service.store()

            if self.translation_enabled:
                self.translation_service.load(
                    source_language_code=source_language_code, target_language_code=target_language_code
                )
                self.translation_service.ref = self.ref
                self.translation_service.store()

        return self.ref


class PronunciationService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(PronunciationService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.PRONUNCIATION,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.limit = 500  # max 500

    def load(self):
        if self.is_expired():
            self.error, self.result = self.wordnik.get_pronunciations(self.word, limit=self.limit)
            if self.error:
                logger.error(f"limit on wordnik.get_pronunciations api")
            else:
                logger.debug(f"wordnik.get_pronunciations: {len(self.result if self.result else [])}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.WORDNIK_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.PRONUNCIATION.value,
                ),
                raw=self.raw if self.raw else self.result,
            )
            self.build_or_create_pronunciations()
        self.update_state()

    def build_or_create_pronunciations(self):
        logger.debug(f"[word: {self.ref}][pronunciations: {len(self.result)}]")
        pers = {}
        for pronunciation in self.result:
            type = pronunciation.rawType
            if type not in pers:
                pers[type] = 0
            if self.limit_enabled and pers[type] >= self.limit_per:
                continue
            self.build_or_create_pronunciation(pronunciation=pronunciation)
            pers[type] = pers[type] + 1

    def build_or_create_pronunciation(self, pronunciation):
        self.source.source = pronunciation.rawType
        logger.debug(f"Pronunciation.objects.get_or_create {self.source.source} {self.ref.word} {pronunciation.raw}")

        pronunciation, created = Pronunciation.objects.get_or_create(
            source=self.source, word=self.ref, pronunciation=pronunciation.raw
        )
        if created:
            logger.debug(f"{pronunciation} [created : {created}]")


class AudioService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(AudioService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.AUDIO,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.limit = 50  # max 50

    def load(self):
        if self.is_expired():
            self.error, self.result = self.wordnik.get_audios(self.word, limit=self.limit)
            if self.error:
                logger.error(f"limit on wordnik.get_audios api")
            else:
                logger.debug(f"wordnik.get_audios: {len(self.result if self.result else [])}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.WORDNIK_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.AUDIO.value,
                ),
                raw=self.raw if self.raw else self.result,
            )
            self.build_or_create_audios()
        self.update_state()

    def build_or_create_audios(self):
        pers = {}
        for audio in self.result:
            created_by = audio.createdBy
            if created_by not in pers:
                pers[created_by] = 0
            if self.limit_enabled and pers[created_by] >= self.limit_per:
                continue
            self.build_or_create_audio(audio=audio)
            pers[created_by] = pers[created_by] + 1

    def build_or_create_audio(self, audio):
        if not audio.createdBy:
            return
        self.source.source = audio.createdBy
        pronunciation, created = Pronunciation.objects.update_or_create(
            source=self.source, word=self.ref, defaults={"url": audio.fileUrl}
        )
        if created:
            logger.debug(f"{pronunciation} [created : {created}]")


class DefinitionService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(DefinitionService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.DEFINITION,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.limit = 500  # max 500

    def load(self):
        if self.is_expired():
            self.error, self.result = self.wordnik.get_definitions(self.word, limit=self.limit)
            if self.error:
                logger.error(f"limit on wordnik.get_definitions api")
            else:
                logger.debug(f"wordnik.get_definitions: {len(self.result if self.result else [])}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.WORDNIK_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.DEFINITION.value,
                ),
                raw=self.raw if self.raw else self.result,
            )
            self.build_or_create_definitions()
        self.update_state()

    def build_or_create_definitions(self):
        pers = {}
        for definition in self.result:
            if None in (definition.sourceDictionary, definition.text):
                continue
            index = definition.sourceDictionary
            if index not in pers:
                pers[index] = 0
            if self.limit_enabled and pers[index] >= self.limit_per:
                continue
            self.build_or_create_definition(definition=definition)
            pers[index] = pers[index] + 1

    def build_or_create_definition(self, definition):
        examples = definition.exampleUses
        self.source.source = definition.sourceDictionary
        part_of_speech = self.get_or_create_part_of_speech(definition.partOfSpeech) if definition.partOfSpeech else None
        attribution = self.get_or_create_attribution(definition.attributionUrl, definition.attributionText)
        definition, created = Definition.objects.get_or_create(
            source=self.source,
            part_of_speech=part_of_speech,
            attribution=attribution,
            word=self.ref,
            definition=definition.text,
        )
        if created:
            logger.debug(f"{definition} [created : {created}]")

        if examples:
            source = self.get_or_create_source(
                type=DictionaryType.DEFINITION,
                subtype=DictionarySubtype.EXAMPLE,
                origin=DictionaryOrigin.WORDNIK_DOT_COM,
            )
            self.build_or_create_examples(source=source, definition=definition, examples=examples)

    def build_or_create_examples(self, source: Source, definition, examples):
        for example in examples:
            self.build_or_create_example(source, definition, example)

    def build_or_create_example(self, source: Source, definition, example):
        example, created = Example.objects.get_or_create(
            source=source, word=self.ref, definition=definition, example=example.text
        )
        if created:
            logger.debug(f"{example} [created : {created}]")


class ExampleService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(ExampleService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.EXAMPLE,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.limit = 50  # max 50

    def load(self):
        if self.is_expired():
            self.error, self.raw = self.wordnik.get_examples(self.word, limit=self.limit)
            self.result = self.raw.examples if hasattr(self.raw, "examples") else None
            if self.error:
                logger.error(f"limit on wordnik.get_examples api")
            else:
                logger.debug(f"wordnik.get_examples: {len(self.result if self.result else [])}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.WORDNIK_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.EXAMPLE.value,
                ),
                raw=self.raw if self.raw else self.result,
            )
            self.build_or_create_examples()
        self.update_state()

    def build_or_create_examples(self):
        for example in self.result:
            self.build_or_create_example(example=example)

    def build_or_create_example(self, example):
        year = f"{example.year}-01-01" if isinstance(example.year, int) else example.year
        example, created = Example.objects.update_or_create(
            source=self.source,
            word=self.ref,
            example=example.text,
            defaults={
                "author": example.author if hasattr(example, "author") else None,
                "title": example.title,
                "url": example.url,
                "year": dateparse.parse_date(year) if year else None,
            },
        )
        if created:
            logger.debug(f"{example} [created : {created}]")


class RelationService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(RelationService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.RELATION,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )
        self.limit = 1000  # max 1000

    def load(self):
        if self.is_expired():
            self.error, self.result = self.wordnik.get_relations(self.word, limit=self.limit)
            if self.error:
                logger.error(f"limit on wordnik.get_relations api")
            else:
                logger.debug(f"wordnik.get_relations: {len(self.result if self.result else [])}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.WORDNIK_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.RELATION.value,
                ),
                raw=self.raw if self.raw else self.result,
            )
            self.build_or_create_relations()
        self.update_state()

    def build_or_create_relations(self):
        for relation in self.result:
            self.build_or_create_relation(relation=relation)

    def build_or_create_relation(self, relation):
        if None in [relation.relationshipType, relation.words]:
            return

        pers = {}
        type = relation.relationshipType

        word_source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.DEFAULT,
            origin=DictionaryOrigin.WORDNIK_DOT_COM,
        )

        language = self.language_service.get_or_create_language(source=word_source)
        relation_type = self.get_or_create_relation_type(source=self.source, relation_type=type)

        for relation_word in relation.words:
            if type not in pers:
                pers[type] = 0
            if self.limit_enabled and pers[type] >= self.limit_per:
                continue
            pers[type] = pers[type] + 1

            relation_word = relation_word.lower()
            relation_word = self.get_or_create_word(source=word_source, language=language, word=relation_word)

            left_word = self.ref if self.ref.id <= relation_word.id else relation_word
            right_word = relation_word if self.ref.id <= relation_word.id else self.ref

            relation, created = Relation.objects.get_or_create(
                source=self.source, relation_type=relation_type, left_word=left_word, right_word=right_word
            )
            if created:
                logger.debug(f"{relation} [created : {created}]")


class TranslationService(Service):
    def __init__(self, ref: Optional[Word], word: str):
        super(TranslationService, self).__init__(ref=ref, word=word)
        self.source = self.get_or_create_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.TRANSLATION,
            origin=DictionaryOrigin.LIBRE_TRANSLATE_DOT_COM,
        )
        self.translator = Translator()

    def load(self, source_language_code: str, target_language_code: str):
        if source_language_code == target_language_code:
            return None

        extra_condition = join_list_in_sort([source_language_code, target_language_code])

        if self.is_expired(extra=extra_condition):
            word_source = self.get_or_create_source(
                type=DictionaryType.WORD,
                subtype=DictionarySubtype.DEFAULT,
                origin=DictionaryOrigin.WORDNIK_DOT_COM,
            )

            # build up languages
            for code in (source_language_code, target_language_code):
                if not self.language_service.has_language(source=word_source, code=code):
                    logger.debug("producing languages for translations")
                    error_languages, languages = self.translator.languages()

                    if not error_languages and languages:
                        for language in languages:
                            self.language_service.get_or_create_language(
                                source=word_source, code=language["code"], name=language["name"]
                            )

            self.source_language = self.language_service.get_language(source=word_source, code=source_language_code)
            self.target_language = self.language_service.get_language(source=word_source, code=target_language_code)

            if self.source_language and self.target_language:
                self.error, self.result = self.translator.translate(
                    text=self.word, source=self.source_language.code, target=self.target_language.code
                )
            if self.error:
                logger.error(f"limit on libretranslate.translate api")
            else:
                logger.debug(f"libretranslate.translate: {self.result}")

    def store(self):
        if self.has_result:
            store_in_lake(
                origin=DictionaryOrigin.LIBRE_TRANSLATE_DOT_COM.value,
                ref=dict(
                    word=self.word,
                    source=self.source_language.code,
                    target=self.target_language.code,
                    type=DictionaryType.WORD.value,
                    subtype=DictionarySubtype.TRANSLATION.value,
                ),
                raw=self.raw if self.raw else self.result,
            )

            word_source = self.get_or_create_source(
                type=DictionaryType.WORD,
                subtype=DictionarySubtype.DEFAULT,
                origin=DictionaryOrigin.WORDNIK_DOT_COM,
            )
            translation = self.get_or_create_word(source=word_source, language=self.target_language, word=self.result)

            self.build_or_create_translation(translation=translation)

        extra_condition = join_list_in_sort([self.source_language.code, self.target_language.code])
        self.update_state(extra=extra_condition)

    def build_or_create_translation(self, translation: Word):
        translation, created = Translation.objects.get_or_create(
            source=self.source,
            source_language=self.source_language,
            target_language=self.target_language,
            source_word=self.ref,
            target_word=translation,
        )
        if created:
            logger.debug(f"{translation} [created : {created}]")
