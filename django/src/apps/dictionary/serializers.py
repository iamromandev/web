from django.db.models import Q

from rest_framework import serializers

from apps.core.models import Language
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
        fields = [
            "id",
            "code",
            "name",
        ]


class PronunciationSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")

    class Meta:
        model = Pronunciation
        fields = [
            "id",
            "source",
            "pronunciation",
            "url",
        ]


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = [
            "id",
            "author",
            "title",
            "example",
            "url",
            "year",
        ]


class DefinitionSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.source")
    part_of_speech = serializers.CharField(source="part_of_speech.part_of_speech")
    examples = ExampleSerializer(many=True)

    class Meta:
        model = Definition
        fields = [
            "id",
            "source",
            "part_of_speech",
            "definition",
            "examples",
        ]


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

    def get_translation(self, word):
        request = self.context.get("request")
        source = request.GET.get("source")
        target = request.GET.get("target")
        source = Language.objects.filter(code=source).first()
        target = Language.objects.filter(code=target).first()
        translation = Translation.objects.filter(source=source, target=target, source_word=word).first()
        return (
            {
                "source": translation.source.code,
                "target": translation.target.code,
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

        return relations

    class Meta:
        model = Word
        fields = [
            "id",
            "language",
            "word",
            "origin",
            "translation",
            "pronunciations",
            "definitions",
            "examples",
            "relations",
        ]
