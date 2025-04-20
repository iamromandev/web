import uuid

from avatar.models import AvatarField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import Address, Code, Language, Platform, Url, User
from apps.core.utils.time_utils import TimezoneChoices


class SocialPlatform(SoftDeleteModel):
    class Type(models.TextChoices):
        FACEBOOK = 'facebook', _('Facebook')
        YOUTUBE = 'youtube', _('YouTube')
        WHATSAPP = 'whatsapp', _('WhatsApp')
        INSTAGRAM = 'instagram', _('Instagram')
        TIKTOK = 'tiktok', _('TikTok')
        WECHAT = 'wechat', _('WeChat')
        FACEBOOK_MESSENGER = 'facebook_messenger', _('Facebook Messenger')
        TELEGRAM = 'telegram', _('Telegram')
        TWITTER = 'twitter', _('X (formerly Twitter)')
        SNAPCHAT = 'snapchat', _('Snapchat')
        PINTEREST = 'pinterest', _('Pinterest')
        LINKEDIN = 'linkedin', _('LinkedIn')
        REDDIT = 'reddit', _('Reddit')
        DISCORD = 'discord', _('Discord')
        TUMBLR = 'tumblr', _('Tumblr')
        THREADS = 'threads', _('Threads')
        BLUESKY = 'bluesky', _('Bluesky')
        MASTODON = 'mastodon', _('Mastodon')
        OTHER = "other", _("Other")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.OneToOneField(
        Platform, on_delete=models.SET_NULL, related_name="social_platform", blank=True, null=True
    )
    type = models.CharField(max_length=32, choices=Type.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["platform__name"]
        verbose_name = _("Social Platform")
        verbose_name_plural = _("Social Platforms")

    def __str__(self):
        return f"[Social Platform: {self.name}, {self.type}]"


class Profile(SoftDeleteModel):
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        NON_BINARY = 'non_binary', _('Non-binary')
        GENDER_FLUID = 'gender_fluid', _('Gender Fluid')
        AGENDER = 'agender', _('Agender')
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')
        OTHER = 'other', _('Other')

    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        PENDING = 'pending', _('Pending')
        SUSPENDED = 'suspended', _('Suspended')
        BLOCKED = 'blocked', _('Blocked')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="profile",
        blank=True,
        null=True,
    )
    display_name = models.CharField(max_length=128, blank=True, null=True)
    avatar = AvatarField(upload_to='profile_avatars/', blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='profile_cover_photos/', blank=True, null=True)
    gender = models.CharField(max_length=32, choices=Gender.choices, blank=True, null=True)
    status = models.CharField(max_length=32, choices=Status.choices, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    phone = PhoneNumberField(blank=True, null=True)
    website_url = models.OneToOneField(
        Url,
        on_delete=models.SET_NULL,
        related_name="profile",
        blank=True,
        null=True,
    )

    languages = models.ManyToManyField(Language, related_name="profiles", blank=True)
    current_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, related_name="current_profiles", blank=True, null=True
    )
    permanent_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, related_name="permanent_profiles", blank=True, null=True
    )

    social_platforms = models.ManyToManyField(SocialPlatform, related_name="profiles", blank=True)
    timezone = models.CharField(
        max_length=128, choices=TimezoneChoices.get_choices(), default="UTC", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"[Profile: {self.display_name}]"


class Verification(SoftDeleteModel):
    class Type(models.TextChoices):
        EMAIL = 'email', _('Email')
        PHONE = 'phone', _('Phone')
        SOCIAL = 'social', _('Social')
        OTHER = 'other', _('Other')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        VERIFIED = 'verified', _('Verified')
        FAILED = 'failed', _('Failed')
        EXPIRED = 'expired', _('Expired')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="registration",
        blank=True,
        null=True,
    )
    type = models.CharField(max_length=32, choices=Type.choices, blank=True, null=True)
    status = models.CharField(max_length=32, choices=Status.choices, blank=True, null=True)
    code = models.OneToOneField(
        Code,
        on_delete=models.SET_NULL,
        related_name="verification",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")

    def __str__(self):
        return f"[Verification: {self.user.username}, {self.type}]"
