from typing import Optional

from django.db.models import Q

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
            "id",
            "code",
            "name",
            "direction",
        )


class PronunciationSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")

    class Meta:
        model = Pronunciation
        fields = (
            "id",
            "source",
            "pronunciation",
            "url",
        )


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = (
            "id",
            "author",
            "title",
            "example",
            "url",
            "year",
        )


class DefinitionSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")
    part_of_speech = serializers.CharField(source="part_of_speech.part_of_speech", allow_blank=True, allow_null=True)
    examples = ExampleSerializer(many=True)

    class Meta:
        model = Definition
        fields = (
            "id",
            "source",
            "part_of_speech",
            "definition",
            "examples",
        )


class WordSerializer(serializers.ModelSerializer):
    # language = serializers.CharField(source='language.code')
    # language = serializers.SlugRelatedField(slug_field='code', read_only=True)
    # language = serializers.RelatedField(read_only=True)
    language = LanguageSerializer(many=False)
    translation = serializers.SerializerMethodField("get_translation")
    pronunciations = PronunciationSerializer(many=True)
    definitions = DefinitionSerializer(many=True)
    # examples = ExampleSerializer(instance=Example.objects.filter(id='222b05d3fa1145a099f980cead65b94c'), many=True)
    examples = serializers.SerializerMethodField("get_examples")
    relations = serializers.SerializerMethodField("get_relations")

    def get_source(
        self,
        type: DictionaryType = DictionaryType.DEFAULT,
        subtype: DictionarySubtype = DictionarySubtype.DEFAULT,
        origin: DictionaryOrigin = DictionaryOrigin.DEFAULT,
        source: Optional[str] = None,
    ) -> Source:
        return Source.objects.filter(type=type.value, subtype=subtype.value, origin=origin.value, source=source).first()

    def get_translation(self, word):
        request = self.context.get("request")
        source_language_code = request.GET.get("source")
        target_language_code = request.GET.get("target")

        source = self.get_source(
            type=DictionaryType.WORD,
            subtype=DictionarySubtype.TRANSLATION,
            origin=DictionaryOrigin.LIBRE_TRANSLATE_DOT_COM,
        )
        source_language = Language.objects.filter(code=source_language_code).first()
        target_language = Language.objects.filter(code=target_language_code).first()
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

    def get_examples(self, word):
        qs = Example.objects.all().filter(word=word, definition=None)
        serializer = ExampleSerializer(instance=qs, many=True)
        return serializer.data

    def get_relations(self, word):
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

    class Meta:
        model = Word
        fields = (
            "id",
            "language",
            "word",
            "translation",
            "pronunciations",
            "definitions",
            "examples",
            "relations",
        )
