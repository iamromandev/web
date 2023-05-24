import uuid

from django.db import models

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, Language


# Create your models here.


class Name(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    simple = models.CharField(max_length=128, blank=True, null=True)
    complex = models.CharField(max_length=128, blank=True, null=True)
    arabic = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["simple"]

    def __str__(self):
        return f'[Name: {self.simple.encode("utf8") if self.simple else self.complex.encode("utf8")}]'


# class Surah(SoftDeleteModel, PolymorphicModel):
#    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#    source = models.ForeignKey(Source, related_name='surahs', on_delete=models.DO_NOTHING)
#    ref_id = models.CharField(max_length=32, blank=True, null=True)
