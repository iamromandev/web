import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, Language


# Create your models here.


# class Resource(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     name = models.CharField(max_length=256, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["name"]
#
#     def __str__(self):
#         return f"[Resource: {self.name}]"
#
#
# class Translation(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     language = models.ForeignKey(Language, related_name="translations", on_delete=models.DO_NOTHING)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"[Translation: {self.source.code}, {self.target.code}, {self.source_word.word.encode('utf8')}, {self.target_word.word.encode('utf8')}]"
#
#
# class Revelation(SoftDeleteModel):
#     class Place(models.TextChoices):
#         MAKKAH = "MAKKAH", _("makkah")
#         MADINA = "MADINA", _("madina")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     place = models.CharField(max_length=8, choices=Place.choices, default=Place.MAKKAH, blank=False, null=False)
#     order = models.PositiveSmallIntegerField(blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["order"]
#
#     def __str__(self):
#         return f"[Revelation: {self.name.encode('utf8')}]"
#
#
# class Surah(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="surahs", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     revelation = models.ForeignKey(Revelation, related_name="surahs", on_delete=models.DO_NOTHING)
#     bismillah = models.BooleanField(blank=False, null=False)
#     ayahs_count = models.PositiveSmallIntegerField(blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["ref_id"]
#
#     def __str__(self):
#         return f"[Surah: {self.name.encode('utf8')}]"
#
#
# class Ayah(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     # text = models.ForeignKey(
#     #     Attribution, related_name="definitions", blank=True, null=True, on_delete=models.DO_NOTHING
#     # )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["ref_id"]
#
#     def __str__(self):
#         return f"[Surah: {self.name.encode('utf8')}]"

# class Word(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="words", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     is_end = models.BooleanField(blank=False, null=False)
#     audio = models.URLField(max_length=256, blank=True, null=True)
#     ayah_key = models.CharField(max_length=16, blank=True, null=True)
#     location = models.CharField(max_length=16, blank=True, null=True)
#     code = models.CharField(max_length=16, blank=True, null=True)
#     position = models.PositiveSmallIntegerField(blank=True, null=True)
#     line = models.PositiveSmallIntegerField(blank=True, null=True)
#     page = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["ref_id"]
#
#     def __str__(self):
#         return f"[Word: {self.id}]"

# class Name(SoftDeleteModel):
#     class Type(models.TextChoices):
#         SIMPLE = "SIMPLE", _("simple")
#         COMPLEX = "COMPLEX", _("complex")
#         ARABIC = "ARABIC", _("arabic")
#         TRANSLATED = "TRANSLATED", _("translated")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     type = models.CharField(max_length=16, choices=Type.choices, default=Type.SIMPLE, blank=False, null=False)
#     language = models.ForeignKey(Language, related_name="surah_names", on_delete=models.DO_NOTHING)
#     name = models.CharField(max_length=128, blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["name"]
#
#     def __str__(self):
#         return f"[Name: {self.name.encode('utf8')}]"
#

#
#
# class Text(SoftDeleteModel):
#     class Script(models.TextChoices):
#         UTHMANI = "UTHMANI", _("uthmani")
#         INDOPAK = "INDOPAK", _("indopak")
#         IMLAEI = "IMLAEI", _("imlaei")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     script = models.CharField(max_length=16, choices=Script.choices, default=Script.UTHMANI, blank=False, null=False)
#     text = models.TextField(blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["script"]
#
#     def __str__(self):
#         return f"[Text: {self.text.encode('utf8')}]"
#
#

#
#
