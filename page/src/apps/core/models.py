import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        """Returns a string representation of the Source instance."""
        return f"[Source: {self.type}, {self.subtype}, {self.source}]"
