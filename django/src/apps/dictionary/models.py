import uuid

from django.db import models

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, Language


# Create your models here.
class PartOfSpeech(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_part_of_speeches", on_delete=models.DO_NOTHING)
    part_of_speech = models.CharField(max_length=64, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["part_of_speech"]

    def __str__(self):
        return f"[PartOfSpeech: {self.part_of_speech}]"


class Word(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_words", on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, related_name="dictionary_words", on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=128, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["word"]

    def __str__(self):
        return f"[Word: {self.word.encode('utf8')}]"


class Pronunciation(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_pronunciations", on_delete=models.DO_NOTHING)
    word = models.ForeignKey(Word, related_name="pronunciations", on_delete=models.DO_NOTHING)
    pronunciation = models.CharField(max_length=256, blank=False, null=False)
    url = models.URLField(max_length=2048, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pronunciation"]

    def __str__(self):
        return f"[Pronunciation: {self.pronunciation.encode('utf8')}]"


class Attribution(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_attributions", on_delete=models.DO_NOTHING)
    url = models.URLField(max_length=2048, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["url"]

    def __str__(self):
        return f"[Attribution: {self.source.code}, {self.target.code}, {self.source_word.word.encode('utf8')}, {self.target_word.word.encode('utf8')}]"


class Definition(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_definitions", on_delete=models.DO_NOTHING)
    part_of_speech = models.ForeignKey(PartOfSpeech, related_name="definitions", on_delete=models.DO_NOTHING)
    attribution = models.ForeignKey(
        Attribution, related_name="definitions", blank=True, null=True, default=None, on_delete=models.DO_NOTHING
    )
    word = models.ForeignKey(Word, related_name="definitions", on_delete=models.DO_NOTHING)
    definition = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["definition"]

    def __str__(self):
        return f"[Definition: {self.definition.encode('utf8')}]"


class Example(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_examples", on_delete=models.DO_NOTHING)
    word = models.ForeignKey(Word, related_name="examples", on_delete=models.DO_NOTHING)
    definition = models.ForeignKey(
        Definition, related_name="examples", blank=True, null=True, default=None, on_delete=models.DO_NOTHING
    )
    author = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    example = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=2048, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["example"]

    def __str__(self):
        return f"[Example: {self.example.encode('utf8')}]"


class RelationType(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_relation_types", on_delete=models.DO_NOTHING)
    relation_type = models.CharField(max_length=64, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["relation_type"]

    def __str__(self):
        return f"[RelationType: {self.relation_type.encode('utf8')}]"


class Relation(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_relations", on_delete=models.DO_NOTHING)
    relation_type = models.ForeignKey(RelationType, related_name="relations", on_delete=models.DO_NOTHING)
    left_word = models.ForeignKey(Word, related_name="left_relations", on_delete=models.DO_NOTHING)
    right_word = models.ForeignKey(Word, related_name="right_relations", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["relation_type"]

    def __str__(self):
        return f"[Relation: {self.relation_type}, {self.left_word}, {self.right_word}]"


class Translation(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="dictionary_translations", on_delete=models.DO_NOTHING)
    source_language = models.ForeignKey(
        Language, related_name="dictionary_source_translations", on_delete=models.DO_NOTHING
    )
    target_language = models.ForeignKey(
        Language, related_name="dictionary_target_translations", on_delete=models.DO_NOTHING
    )
    source_word = models.ForeignKey(Word, related_name="source_word_translations", on_delete=models.DO_NOTHING)
    target_word = models.ForeignKey(Word, related_name="target_word_translations", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source"]

    def __str__(self):
        return f"[Translation: {self.source_language.code}, {self.target_language.code}, {self.source_word.word.encode('utf8')}, {self.target_word.word.encode('utf8')}]"
