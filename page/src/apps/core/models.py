import uuid
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


# Create your models here.
class Tag(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


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
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __str__(self) -> str:
        """Returns a string representation of the Source instance."""
        return f"[Source: {self.type}, {self.subtype}, {self.origin}, {self.source}]"


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref = models.UUIDField(editable=False, blank=False, null=False)
    source = models.ForeignKey(
        Source, on_delete=models.DO_NOTHING, related_name="states"
    )
    state = models.CharField(max_length=32, blank=False, null=False)
    extra = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source", "state"]
        unique_together = [("ref", "source")]
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return f"[State: {self.source}, {self.state}]"

    def is_expired(self, delay_s: int) -> bool:
        return (timezone.now() - self.updated_at).total_seconds() > delay_s


class Code(SoftDeleteModel):
    class Type(models.TextChoices):
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
        max_length=32, choices=Type.choices, blank=True, null=True
    )
    code = models.CharField(max_length=64, blank=False, null=False, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = _("Code")
        verbose_name_plural = _("Codes")

    def __str__(self):
        return f"[Code: {self.source}, {self.code}]"


class Language(SoftDeleteModel):
    class Direction(models.TextChoices):
        LTR = "LTR", _("Left to Right")
        RTL = "RTL", _("Right to Left")

    class Script(models.TextChoices):
        LATIN = 'latin', _('Latin')
        CYRILLIC = 'cyrillic', _('Cyrillic')
        ARABIC = 'arabic', _('Arabic')
        DEVANAGARI = 'devanagari', _('Devanagari')
        CHINESE = 'chinese', _('Chinese')
        GREEK = 'greek', _('Greek')
        HEBREW = 'hebrew', _('Hebrew')
        JAPANESE = 'japanese', _('Japanese')
        KOREAN = 'korean', _('Korean')
        THAI = 'thai', _('Thai')
        TAMIL = 'tamil', _('Tamil')
        BENGALI = 'bengali', _('Bengali')
        BRAILLE = 'braille', _('Braille')
        ETHIOPIC = 'ethiopic', _('Ethiopic')
        GEORGIAN = 'georgian', _('Georgian')
        MONGOLIAN = 'mongolian', _('Mongolian')
        SYRIAC = 'syriac', _('Syriac')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    native_name = models.CharField(max_length=256, blank=True, null=True)
    direction = models.CharField(
        max_length=3, choices=Direction.choices, default=Direction.LTR
    )
    codes = models.ManyToManyField(Code, related_name="languages", blank=True, null=True)
    script = models.CharField(max_length=32, choices=Script.choices, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"[Language: {self.source}, {self.code}, {self.name}]"


class Coordinate(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("latitude", "longitude")
        unique_together = ("latitude", "longitude")
        verbose_name = _("Coordinate")
        verbose_name_plural = _("Coordinates")

    def __str__(self):
        return f"[Coordinate: {self.latitude}, {self.longitude}]"


class Location(SoftDeleteModel):
    class Type(models.TextChoices):
        COUNTRY = "country", _("Country")
        STATE_PROVINCE = "state_province", _("State/Province")
        DIVISION = 'division', _('Division')
        DISTRICT = 'district', _('District')
        CITY = "city", _("City")
        COUNTY = "county", _("County")
        UPAZILA = 'upazila', _('Upazila')
        UNION = 'union', _('Union')
        MUNICIPALITY = "municipality", _("Municipality")
        CITY_CORPORATION = 'city_corporation', _('City Corporation')
        TOWN = 'town', _('Town')
        VILLAGE = 'village', _('Village')
        REGION = 'region', 'Region'
        ADDRESS = 'address', 'Address'
        TERRITORY = "territory", _("Territory")
        AUTONOMOUS_REGION = "autonomous_region", _("Autonomous Region")
        UNION_TERRITORY = "union_territory", _("Union Territory")
        PREFECTURE = "prefecture", _("Prefecture")
        ZONE = "zone", _("Zone")
        POSTAL = "postal", _("Postal")
        NEIGHBORHOOD = 'neighborhood', _('Neighborhood')
        LANDMARK = 'landmark', _('Landmark')
        OTHER = 'other', _('Other')

    class Continent(models.TextChoices):
        AFRICA = 'africa', _('Africa')
        ANTARCTICA = 'antarctica', _('Antarctica')
        ASIA = 'asia', _('Asia')
        EUROPE = 'europe', _('Europe')
        NORTH_AMERICA = 'north_america', _('North America')
        SOUTH_AMERICA = 'south_america', _('South America')
        AUSTRALIA_OCEANIA = 'australia_oceania', _('Australia/Oceania')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="children")
    name = models.CharField(max_length=256, unique=True, blank=False, null=False)
    type = models.CharField(
        max_length=32, choices=Type.choices, blank=True, null=True
    )
    continent = models.CharField(
        max_length=32, choices=Continent.choices, blank=True, null=True
    )
    coordinate = models.ForeignKey(
        Coordinate, blank=True, null=True, on_delete=models.SET_NULL, related_name="locations"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_location_type_display(self) -> Optional[str]:
        return Location.LocationType.choices.get(self.type, self.type)

    def __str__(self):
        return f"[Location: {self.name}, {self.location}]"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")


class Address(SoftDeleteModel):
    class Type(models.TextChoices):
        BILLING = "BILLING", _("Billing")
        SHIPPING = "SHIPPING", _("Shipping")
        HOME = "HOME", _("Home")
        WORK = "WORK", _("Work")
        OFFICE = "OFFICE", _("Office")
        PO_BOX = "PO_BOX", _("PO Box")
        DELIVERY = "DELIVERY", _("Delivery")
        MAILING = "MAILING", _("Mailing")
        TEMPORARY = "TEMPORARY", _("Temporary")
        OTHER = "OTHER", _("Other")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="addresses", blank=True, null=True
    )
    type = models.CharField(
        max_length=32, choices=Type.choices, blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=256, blank=False, null=False)
    address_line_2 = models.CharField(max_length=256, blank=True, null=True)
    locations = models.ManyToManyField(Location, related_name="addresses", blank=True, null=True)
    coordinate = models.ForeignKey(
        Coordinate, blank=True, null=True, on_delete=models.SET_NULL, related_name="addresses"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[Address: {self.name}, {self.location}]"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
