import uuid

from django.db import models

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source


# Create your models here.
class File(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="media_files", on_delete=models.DO_NOTHING)
    path = models.CharField(max_length=512, blank=False, null=False)
    size = models.PositiveIntegerField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("path",)


class Image(SoftDeleteModel):
    file = models.OneToOneField(File, primary_key=True, on_delete=models.CASCADE)
    width = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    height = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("file",)
