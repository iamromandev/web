import uuid
from contextlib import nullcontext

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


# Create your models here.
class Tag(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")


class User(SoftDeleteModel, AbstractUser):
    # Django's AbstractUser already includes the following fields by default:
    # - id (AutoField, primary key)
    # - password
    # - last_login
    # - is_superuser
    # - username
    # - first_name
    # - last_name
    # - email
    # - is_staff
    # - is_active
    # - date_joined
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"[User: {self.username} {self.email}]"


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=32, blank=False, null=False)
    subtype = models.CharField(max_length=32, blank=False, null=False)
    origin = models.CharField(max_length=32, blank=False, null=False)
    source = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source"]
        verbose_name = _("source")
        verbose_name_plural = _("sources")

    def __str__(self) -> str:
        """Returns a string representation of the Source instance."""
        return f"[Source: {self.type}, {self.subtype}, {self.origin}, {self.source}]"


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.UUIDField(editable=True, blank=False, null=False)
    source = models.ForeignKey(
        Source,
        on_delete=models.DO_NOTHING,
        related_name="states",
    )
    state = models.CharField(max_length=32, blank=False, null=False)
    extra = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source", "state"]
        unique_together = [("ref", "source")]
        verbose_name = _("state")
        verbose_name_plural = _("states")

    def __str__(self):
        return f"[State: {self.source}, {self.state}]"

    def is_expired(self, delay_s: int) -> bool:
        return (timezone.now() - self.updated_at).total_seconds() > delay_s


class Code(SoftDeleteModel):

    class CodeType(models.TextChoices):
        REGION = "region", _("Region Code")
        COUNTRY = "country", _("Country Code")
        STATE_PROVINCE = "state_province", _("State/Province Code")
        CITY = "city", _("City Code")
        STATUS = "status", _("Status Code")
        ERROR = "error", _("Error Code")
        PRODUCT = "product", _("Product Code")
        ORDER = "order", _("Order Code")
        SHIPPING = "shipping", _("Shipping Code")
        PAYMENT = "payment", _("Payment Code")
        CURRENCY = "currency", _("Currency Code")
        LANGUAGE = "language", _("Language Code")
        PRIORITY = "priority", _("Priority Code")
        ROLE = "role", _("Role Code")
        CATEGORY = "category", _("Category Code")
        EVENT = "event", _("Event Code")
        LICENSE = "license", _("License Code")
        DISCOUNT = "discount", _("Discount Code")
        TAX = "tax", _("Tax Code")
        COLOR = "color", _("Color Code")
        POSTAL = "postal", _("Postal Code")
        INTERNAL = "internal", _("Internal Code")
        ISO_3166_1_ALPHA2 = "iso_alpha2", _("ISO 3166-1 Alpha-2")
        ISO_3166_1_ALPHA3 = "iso_alpha3", _("ISO 3166-1 Alpha-3")
        ISO_3166_1_NUMERIC = "iso_numeric", _("ISO 3166-1 Numeric")
        ISO_3166_2 = "iso_3166_2", _("ISO 3166-2")
        ISO_639_1 = "iso_639_1", _("ISO 639-1 Language")
        ISO_4217 = "iso_4217", _("ISO 4217 Currency")
        ISO_8601 = "iso_8601", "ISO 8601 Date/Time"
        ISO_15924 = "iso_15924", _("ISO 15924 Script")
        OTHER = "other", _("Other Code")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=32, choices=CodeType.choices, blank=True, null=True
    )
    code = models.CharField(max_length=64, blank=False, null=False, db_index=True)
    desc = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = _("code")
        verbose_name_plural = _("codes")

    def __str__(self):
        return f"[Code: {self.source}, {self.code}]"

# class Region(SoftDeleteModel):
#     class Continent(models.TextChoices):
#         AFRICA = 'africa', _('Africa')
#         ANTARCTICA = 'antarctica', _('Antarctica')
#         ASIA = 'asia', _('Asia')
#         EUROPE = 'europe', _('Europe')
#         NORTH_AMERICA = 'north_america', _('North America')
#         SOUTH_AMERICA = 'south_america', _('South America')
#         AUSTRALIA_OCEANIA = 'australia_oceania', _('Australia/Oceania')
#
#     class RegionType(models.TextChoices):
#         COUNTRY = 'country', _('Country')
#         STATE_PROVINCE = 'state_province', _('State/Province')
#         DIVISION = 'division', _('Division')
#         DISTRICT = 'district', _('District')
#         CITY = 'city', _('City')
#         COUNTY = 'county', _('County')  # Upazila, sub-district, etc.
#         MUNICIPALITY = 'municipality', _('Municipality')  # city corporation
#         TERRITORY = 'territory', _('Territory')
#         AUTONOMOUS_REGION = 'autonomous_region', _('Autonomous Region')
#         UNION_TERRITORY = 'union_territory', _('Union Territory')
#         PREFECTURE = 'prefecture', _('Prefecture')
#         ZONE = 'zone', _('Zone')
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="children")
#     name = models.CharField(max_length=256, unique=True, blank=False, null=False)
#
#     type = models.CharField(
#         max_length=32, choices=RegionType.choices, default=RegionType.COUNTRY
#     )
#     code = models.CharField(max_length=8, unique=True, blank=False)
#     continent = models.CharField(
#         max_length=2, choices=Continent.choices, default=Continent.ASIA
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["name"]
#         verbose_name = _("region")
#         verbose_name_plural = _("regions")
#
#     def __str__(self):
#         return f"[Region: {self.source}, {self.code}, {self.name}]"

#
# class Language(SoftDeleteModel):
#     class Direction(models.TextChoices):
#         LTR = "LTR", _("Left to Right")
#         RTL = "RTL", _("Right to Left")
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     source = models.ForeignKey(
#         Source, on_delete=models.DO_NOTHING, related_name="languages"
#     )
#     name = models.CharField(max_length=128, blank=False, null=False)
#     direction = models.CharField(
#         max_length=3, choices=Direction.choices, default=Direction.LTR
#     )
#     code = models.CharField(max_length=8, unique=True, blank=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["name"]
#         verbose_name = _("Language")
#         verbose_name_plural = _("Languages")
#
#     def __str__(self):
#         return f"[Language: {self.source}, {self.code}, {self.name}]"
