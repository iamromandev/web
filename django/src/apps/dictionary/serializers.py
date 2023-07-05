from typing import Optional

from django.db.models import Q

from loguru import logger
from rest_framework import serializers

from apps.core.models import Source, Language
from apps.dictionary.enums import (
    Type as DictionaryType,
    Subtype as DictionarySubtype,
    Origin as DictionaryOrigin,
    State as DictionaryState,
)
from apps.dictionary.models import (
    Pronunciation,
    Example,
    Definition,
    Word,
    Relation,
    Translation,
)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            "code",
            "name",
            "direction",
        )


class PronunciationSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")

    class Meta:
        model = Pronunciation
        fields = (
            "source",
            "pronunciation",
            "url",
        )


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = (
            "author",
            "title",
            "example",
            "url",
            "year",
        )


class DefinitionSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")
    part_of_speech = serializers.CharField(source="part_of_speech.part_of_speech", allow_blank=True, allow_null=True)
    # examples = ExampleSerializer(many=True)
    examples = serializers.SerializerMethodField("get_examples")

    class Meta:
        model = Definition
        fields = (
            "source",
            "part_of_speech",
            "definition",
            "examples",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        basic = request.GET.get("basic", "false")
        self.basic = True if "true" == basic else False

    def get_examples(self, definition):
        if self.basic:
            data = None
        else:
            # definition=None for only examples associated with word and without definition
            qs = Example.objects.filter(definition=definition)
            serializer = ExampleSerializer(instance=qs, many=True)
            data = serializer.data
        return data


class WordSerializer(serializers.ModelSerializer):
    # language = serializers.CharField(source='language.code')
    # language = serializers.SlugRelatedField(slug_field='code', read_only=True)
    # language = serializers.RelatedField(read_only=True)
    language = LanguageSerializer(many=False)
    translation = serializers.SerializerMethodField("get_translation")
    pronunciations = PronunciationSerializer(many=True)
    # definitions = DefinitionSerializer(many=True)
    definitions = serializers.SerializerMethodField("get_definitions")  # for applying limit
    # examples = ExampleSerializer(instance=Example.objects.filter(id='222b05d3fa1145a099f980cead65b94c'), many=True)
    examples = serializers.SerializerMethodField("get_examples")
    relations = serializers.SerializerMethodField("get_relations")

    class Meta:
        model = Word
        fields = (
            "language",
            "word",
            "translation",
            "pronunciations",
            "definitions",
            "examples",
            "relations",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        self.source = request.GET.get("source", "en")
        self.target = request.GET.get("target", "en")
        basic = request.GET.get("basic", "false")
        self.basic = True if "true" == basic else False

        # We pass the "upper serializer" context to the "nested one"
        # self.fields["definitions"].context.update(self.context)

    def get_source(
        self,
        type: DictionaryType = DictionaryType.DEFAULT,
        subtype: DictionarySubtype = DictionarySubtype.DEFAULT,
        origin: DictionaryOrigin = DictionaryOrigin.DEFAULT,
        source: Optional[str] = None,
    ) -> Source:
        return Source.objects.filter(type=type.value, subtype=subtype.value, origin=origin.value, source=source).first()

    def get_translation(self, word):
        if self.basic:
            translation = None
        else:
            source = self.get_source(
                type=DictionaryType.WORD,
                subtype=DictionarySubtype.TRANSLATION,
                origin=DictionaryOrigin.LIBRE_TRANSLATE_DOT_COM,
            )
            source_language = Language.objects.filter(code=self.source).first()
            target_language = Language.objects.filter(code=self.target).first()
            translation = Translation.objects.filter(
                source=source, source_language=source_language, target_language=target_language, source_word=word
            ).first()
        return (
            {
                "source": translation.source_language.code,
                "target": translation.target_language.code,
                "translation": translation.target_word.word,
            }
            if translation
            else None
        )

    def get_definitions(self, word):
        qs = Definition.objects.filter(word=word)
        if self.basic:
            qs = qs.order_by("-created_at")[:3]
        context = {"request": self.context.get("request")}
        serializer = DefinitionSerializer(instance=qs, many=True, context=context)
        data = serializer.data
        return data

    def get_examples(self, word):
        if self.basic:
            data = None
        else:
            # definition=None for only examples associated with word and without definition
            qs = Example.objects.filter(word=word, definition=None)
            serializer = ExampleSerializer(instance=qs, many=True)
            data = serializer.data
        return data

    def get_relations(self, word):
        if self.basic:
            result = None
        else:
            relations = {}

            relation_qs = Relation.objects.all().filter(Q(left_word=word.id) | Q(right_word=word.id)).all()

            for relation in relation_qs:
                relation_word = relation.right_word if relation.left_word.id == word.id else relation.left_word
                relation_type = relation.relation_type.relation_type
                if relation_type not in relations:
                    relations[relation_type] = {}
                relations[relation_type][str(relation_word.id)] = relation_word.word

            result = {}

            for type, type_words in relations.items():
                result[type] = list(type_words.values())
                result[type].sort()

        return result
