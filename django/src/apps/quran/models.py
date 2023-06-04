import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, Language


# Create your models here.


# class Resource(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_resources", on_delete=models.DO_NOTHING)
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
#     source = models.ForeignKey(Source, related_name="quran_translations", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     language = models.ForeignKey(Language, related_name="quran_translations", on_delete=models.DO_NOTHING)
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
#     source = models.ForeignKey(Source, related_name="quran_revelations", on_delete=models.DO_NOTHING)
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
#     source = models.ForeignKey(Source, related_name="quran_surahs", on_delete=models.DO_NOTHING)
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
# class Name(SoftDeleteModel):
#     class Type(models.TextChoices):
#         SIMPLE = "SIMPLE", _("simple")
#         COMPLEX = "COMPLEX", _("complex")
#         ARABIC = "ARABIC", _("arabic")
#         TRANSLATED = "TRANSLATED", _("translated")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_names", on_delete=models.DO_NOTHING)
#     surah = models.ForeignKey(Surah, blank=True, null=True, default=None, related_name="names", on_delete=models.DO_NOTHING)
#     type = models.CharField(max_length=16, choices=Type.choices, default=Type.SIMPLE, blank=False, null=False)
#     language = models.ForeignKey(Language, related_name="quran_surah_names", on_delete=models.DO_NOTHING)
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
# class Page(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     ref = models.UUIDField(editable=False, default=uuid.uuid4)
#     type = models.CharField(max_length=32, blank=False, null=False)
#     subtype = models.CharField(max_length=32, blank=False, null=False)
#     surah = models.ForeignKey(Surah, related_name="pages", on_delete=models.DO_NOTHING)
#     page = models.PositiveSmallIntegerField(blank=False, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["page"]
#
#     def __str__(self):
#         return f"[Page: {self.page}, Surah: {self.surah.ref_id}]"
#
#
# class Juz(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_juzs", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     number = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["number"]
#
#     def __str__(self):
#         return f"[Juz: {self.number}]"
#
#
# class Hizb(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_hizbs", on_delete=models.DO_NOTHING)
#     juz = models.ForeignKey(Juz, related_name="hizbs", on_delete=models.DO_NOTHING)
#     number = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["number"]
#
#     def __str__(self):
#         return f"[Hizb: {self.number}]"
#
#
# class Rub(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_rubs", on_delete=models.DO_NOTHING)
#     hizb = models.ForeignKey(Hizb, related_name="rubs", on_delete=models.DO_NOTHING)
#     number = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["number"]
#
#     def __str__(self):
#         return f"[Rub: {self.number}]"
#
#
# class Sajdah(SoftDeleteModel):
#     class Type(models.TextChoices):
#         SALAAH = "SALAAH", _("salaah")
#         SAHW = "SAHW", _("sahw")
#         TILAAWAH = "TILAAWAH", _("tilaawah")
#         SHUKR = "SHUKR", _("shukr")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_sajdahs", on_delete=models.DO_NOTHING)
#     type = models.CharField(max_length=16, choices=Type.choices, default=Type.SALAAH, blank=False, null=False)
#     number = models.PositiveSmallIntegerField(blank=True, null=True)
#     juz = models.ForeignKey(Juz, related_name="sajdahs", on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["number"]
#
#     def __str__(self):
#         return f"[Sajdah: {self.number}]"
#
#
# class Ayah(SoftDeleteModel):
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_ayahs", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
#     surah = models.ForeignKey(Surah, related_name="ayahs", on_delete=models.DO_NOTHING)
#     juz = models.ForeignKey(Juz, related_name="ayahs", on_delete=models.DO_NOTHING)
#     hizb = models.ForeignKey(Hizb, related_name="ayahs", on_delete=models.DO_NOTHING)
#     rub = models.ForeignKey(Rub, related_name="ayahs", on_delete=models.DO_NOTHING)
#     number = models.PositiveSmallIntegerField(blank=False, null=False)
#     key = models.CharField(max_length=32, blank=True, null=True)
#     index = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["ref_id"]
#
#     def __str__(self):
#         return f"[Ayah: {self.number}]"
#
#
# class Sajdah(SoftDeleteModel):
#     class Type(models.TextChoices):
#         SALAAH = "SALAAH", _("salaah")
#         SAHW = "SAHW", _("sahw")
#         TILAAWAH = "TILAAWAH", _("tilaawah")
#         SHUKR = "SHUKR", _("shukr")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_sajdahs", on_delete=models.DO_NOTHING)
#     type = models.CharField(max_length=16, choices=Type.choices, default=Type.SALAAH, blank=False, null=False)
#     number = models.PositiveSmallIntegerField(blank=True, null=True)
#     juz = models.ForeignKey(Juz, related_name="sajdahs", on_delete=models.DO_NOTHING)
#     surah = models.ForeignKey(Surah, related_name="sajdahs", on_delete=models.DO_NOTHING)
#     ayah = models.ForeignKey(Ayah, related_name="sajdahs", on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["number"]
#
#     def __str__(self):
#         return f"[Sajdah: {self.number}]"
#
#
# class Text(SoftDeleteModel):
#     class Script(models.TextChoices):
#         UTHMANI = "UTHMANI", _("uthmani")
#         UTHMANI_SIMPLE = "UTHMANI_SIMPLE", _("uthmani_simple")
#         UTHMANI_TAJWEED = "UTHMANI_TAJWEED", _("uthmani_tajweed")
#         INDOPAK = "INDOPAK", _("indopak")
#         IMLAEI = "IMLAEI", _("imlaei")
#         IMLAEI_SIMPLE = "IMLAEI_SIMPLE", _("imlaei_simple")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="quran_texts", on_delete=models.DO_NOTHING)
#     ref_id = models.CharField(max_length=32, blank=True, null=True)
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


#

#
#

#
#

#
#
