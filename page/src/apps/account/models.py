import uuid

from avatar.models import AvatarField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField

#from apps.core.models import Address, Code, Language, User
from apps.core.time_utils import TimezoneChoices


# class Profile(SoftDeleteModel):
#     class Gender(models.TextChoices):
#         MALE = 'male', _('Male')
#         FEMALE = 'female', _('Female')
#         NON_BINARY = 'non_binary', _('Non-binary')
#         GENDER_FLUID = 'gender_fluid', _('Gender Fluid')
#         AGENDER = 'agender', _('Agender')
#         PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')
#         OTHER = 'other', _('Other')
#
#     class Status(models.TextChoices):
#         ACTIVE = 'active', _('Active')
#         INACTIVE = 'inactive', _('Inactive')
#         PENDING = 'pending', _('Pending')
#         SUSPENDED = 'suspended', _('Suspended')
#         BLOCKED = 'blocked', _('Blocked')
#
#     user = models.OneToOneField(
#         User,
#         on_delete=models.SET_NULL,
#         related_name="profile",
#         blank=True,
#         null=True,
#     )
#
#     display_name = models.CharField(max_length=128, blank=True, null=True)
#     avatar = AvatarField(upload_to='profile_avatars/', blank=True, null=True)
#     photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
#     cover_photo = models.ImageField(upload_to='profile_cover_photos/', blank=True, null=True)
#     gender = models.CharField(max_length=32, choices=Gender.choices, blank=True, null=True)
#     status = models.CharField(max_length=32, choices=Status.choices,  blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     birthdate = models.DateField(blank=True, null=True)
#
#     phone = PhoneNumberField(blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#
#     languages = models.ManyToManyField(Language, related_name="profiles", blank=True)
#     current_address = models.ForeignKey(
#         Address, on_delete=models.SET_NULL, related_name="current_profiles", blank=True, null=True
#     )
#     permanent_address = models.ForeignKey(
#         Address, on_delete=models.SET_NULL, related_name="permanent_profiles", blank=True, null=True
#     )
#     timezone = TimeZoneField(choices=TimezoneChoices.get_choices(), default="UTC", blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["display_name"]
#         verbose_name = _("Profile")
#         verbose_name_plural = _("Profiles")
