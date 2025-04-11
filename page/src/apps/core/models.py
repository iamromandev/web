import uuid
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class Tag(SoftDeleteModel, GenericUUIDTaggedItemBase, TaggedItemBase):
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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"[User: {self.username} {self.email}]"


class Source(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    type = models.CharField(max_length=32, blank=False, null=False)
    subtype = models.CharField(max_length=32, blank=False, null=False)
    origin = models.CharField(max_length=32, blank=False, null=False)
    source = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["type", "subtype", "origin"]
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __str__(self) -> str:
        """Returns a string representation of the Source instance."""
        return f"[Source: {self.type}, {self.subtype}, {self.origin}, {self.source}]"


class State(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ref = models.UUIDField(editable=False, blank=False, null=False)
    source = models.ForeignKey(
        Source, on_delete=models.DO_NOTHING, related_name="states", blank=False, null=False
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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
        LTR = "ltr", _("Left to Right")
        RTL = "rtl", _("Right to Left")

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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=False, null=False)
    native_name = models.CharField(max_length=128, blank=True, null=True)
    direction = models.CharField(
        max_length=3, choices=Direction.choices, default=Direction.LTR
    )
    codes = models.ManyToManyField(Code, related_name="languages", blank=True)
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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="children", blank=True, null=True
    )
    name = models.CharField(max_length=128, unique=True, blank=False, null=False)
    type = models.CharField(
        max_length=32, choices=Type.choices, blank=True, null=True
    )
    continent = models.CharField(
        max_length=32, choices=Continent.choices, blank=True, null=True
    )
    coordinate = models.ForeignKey(
        Coordinate, on_delete=models.SET_NULL, related_name="locations", blank=True, null=True
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
        BILLING = "billing", _("Billing")
        SHIPPING = "shipping", _("Shipping")
        HOME = "home", _("Home")
        WORK = "work", _("Work")
        OFFICE = "office", _("Office")
        PO_BOX = "po_box", _("PO Box")
        DELIVERY = "delivery", _("Delivery")
        MAILING = "mailing", _("Mailing")
        TEMPORARY = "temporary", _("Temporary")
        OTHER = "other", _("Other")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="addresses", blank=True, null=True
    )
    type = models.CharField(
        max_length=32, choices=Type.choices, blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=256, blank=False, null=False)
    address_line_2 = models.CharField(max_length=256, blank=True, null=True)
    locations = models.ManyToManyField(Location, related_name="addresses", blank=True)
    coordinate = models.ForeignKey(
        Coordinate, on_delete=models.SET_NULL, related_name="addresses", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[Address: {self.name}, {self.location}]"

    class Meta:
        ordering = ["address_line_1"]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Url(SoftDeleteModel):
    class Type(models.TextChoices):
        TERMS_OF_SERVICE = 'terms_of_service', _('Terms of Service')
        PRIVACY_POLICY = 'privacy_policy', _('Privacy Policy')
        COOKIE_POLICY = 'cookie_policy', _('Cookie Policy')
        REFUND_POLICY = 'refund_policy', _('Refund Policy')
        RETURN_POLICY = 'return_policy', _('Return Policy')
        COMMUNITY_GUIDELINES = 'community_guidelines', _('Community Guidelines')
        DISPUTE_RESOLUTION = 'dispute_resolution', _('Dispute Resolution Policy')
        GDPR_COMPLIANCE = 'gdpr_compliance', _('GDPR Compliance')
        EULA = 'eula', _('End User License Agreement')
        AUP = 'aup', _('Acceptable Use Policy')
        SLA = 'sla', _('Service Level Agreement')
        API_DOCS = 'api_docs', _('API Documentation')
        API_TERMS = 'api_terms', _('API Terms of Use')
        DEVELOPER_PORTAL = 'developer_portal', _('Developer Portal')
        SUPPORT_CENTER = 'support_center', _('Support Center')
        CONTACT_US = 'contact_us', _('Contact Us')
        HELP_CENTER = 'help_center', _('Help Center')
        SECURITY_POLICY = 'security_policy', _('Security Policy')
        TRUST_CENTER = 'trust_center', _('Trust Center')
        BUG_BOUNTY = 'bug_bounty', _('Bug Bounty Program')
        PRICING = 'pricing', _('Pricing')
        PROMOTIONS = 'promotions', _('Promotions')
        CASE_STUDIES = 'case_studies', _('Case Studies')
        ABOUT_US = 'about_us', _('About Us')
        CAREERS = 'careers', _('Careers')
        PRESS_KIT = 'press_kit', _('Press Kit')
        BLOG = 'blog', _('Blog')
        WEBSITE = 'website', _('Website')
        SOCIAL_MEDIA = 'social_media', _('Social Media')
        # FACEBOOK = 'facebook', _('Facebook')
        # TWITTER = 'twitter', _('Twitter')
        # LINKEDIN = 'linkedin', _('LinkedIn')
        # DISCORD = 'discord', _('Discord')
        # YOUTUBE = 'youtube', _('YouTube')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    url = models.URLField(unique=True, blank=False, null=False)
    type = models.CharField(max_length=32, choices=Type.choices, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name="urls", blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["url"]
        verbose_name = _("URL")
        verbose_name_plural = _("URLs")

    def __str__(self):
        return f"[URL: {self.url}]"

# class Platform(SoftDeleteModel):
#     class Type(models.TextChoices):
#         SOCIAL_MEDIA = 'SOCIAL_MEDIA', _('Social Networking (e.g., Facebook, Instagram)')
#         STREAMING = 'streaming', _('Video/Audio Streaming (e.g., YouTube, Netflix)')
#         MESSAGING = 'messaging', _('Instant Messaging (e.g., WhatsApp, Telegram)')
#         BLOGGING = 'blogging', _('Content Publishing (e.g., Medium, WordPress)')
#         FORUMS = 'forums', _('Community Discussion (e.g., Reddit, Quora)')
#         GAMING = 'gaming', _('Video Game Platforms (e.g., Steam, PlayStation)')
#         ECOMMERCE = 'ecommerce', _('Online Shopping (e.g., Amazon, Shopify)')
#         BUSINESS = 'business', _('Workplace Tools (e.g., Slack, Salesforce)')
#         EDUCATION = 'education', _('Learning Environments (e.g., Coursera, Moodle)')
#         ENTERTAINMENT = 'entertainment', _('Media Consumption (e.g., Spotify, Netflix)')
#         DEVELOPER = 'developer', _('Software Development (e.g., GitHub, AWS)')
#         HEALTH_FITNESS = 'health_fitness', _('Wellness and Fitness (e.g., Fitbit, Calm)')
#         FINANCIAL = 'financial', _('Financial Management (e.g., PayPal, Robinhood)')
#         CROWDFUNDING = 'crowdfunding', _('Fundraising Platforms (e.g., Kickstarter)')
#         TRAVEL_BOOKING = 'travel_booking', _('Travel Services (e.g., Expedia, Airbnb)')
#         REAL_ESTATE = 'real_estate', _('Property Listings (e.g., Zillow, Realtor.com)')
#         DATING = 'dating', _('Online Dating (e.g., Tinder, Bumble)')
#         NEWS_AGGREGATOR = 'news_aggregator', _('News Collection (e.g., Flipboard, Feedly)')
#         OTHER = "other", _("Other")
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=128, unique=True, blank=False, null=False)
#     slug = models.SlugField(max_length=128, unique=True, blank=False, null=False)
#     type = models.CharField(max_length=32, choices=Type.choices, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     logo = models.ImageField(upload_to="platform_logos/", blank=True, null=True)
#     founded_date = models.DateField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"[Platform: {self.name}, {self.type}]"
#
#     class Meta:
#         ordering = ["name"]
#         verbose_name = _("Platform")
#         verbose_name_plural = _("Platforms")
