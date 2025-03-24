import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import Source


class Country(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(
        Source, related_name="account_countries", on_delete=models.DO_NOTHING
    )
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=128, unique=True)
    official_name = models.CharField(max_length=128, blank=True, null=True)
    iso3 = models.CharField(max_length=3, unique=True, verbose_name=_("ISO3 Code"))
    numeric_code = models.CharField(max_length=3, blank=True, null=True)
    phone_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
