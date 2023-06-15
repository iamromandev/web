import uuid

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase
from django_softdelete.models import SoftDeleteModel


# Create your models here.


class Tag(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"[User: {self.username} {self.email}]"


class Source(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    type = models.CharField(max_length=32, blank=False, null=False)
    subtype = models.CharField(max_length=32, blank=False, null=False)
    origin = models.CharField(max_length=32, blank=False, null=False)
    source = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source"]

    def __str__(self):
        return f"[Source: {self.type}, {self.subtype}, {self.source}]"


class Language(SoftDeleteModel):
    class Direction(models.TextChoices):
        LTR = "LTR", _("left-to-right")
        RTL = "RTL", _("right-to-left")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="languages", on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=8, blank=False, null=False)
    origin = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    direction = models.CharField(max_length=8, choices=Direction.choices, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"[Language: {self.source}, {self.code}, {self.name}]"


class State(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ref = models.UUIDField(editable=True, blank=False, null=False)
    source = models.ForeignKey(Source, related_name="states", on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=32, blank=False, null=False)
    extra = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source"]
        unique_together = [("ref", "source")]

    def __str__(self):
        return f"[State: {self.source}, {self.state}]"

    def is_expired(self, delay_s: int):
        return int(timezone.now().timestamp()) - int(self.updated_at.timestamp()) > delay_s
