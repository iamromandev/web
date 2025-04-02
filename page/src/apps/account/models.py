import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from phonenumber_field.modelfields import PhoneNumberField

#from apps.core.models import Code, Language, User


# class Profile(SoftDeleteModel):
#     class Gender(models.TextChoices):
#         MALE = 'male', _('Male')
#         FEMALE = 'female', _('Female')
#         NON_BINARY = 'non_binary', _('Non-binary')
#         GENDER_FLUID = 'gender_fluid', _('Gender Fluid')
#         AGENDER = 'agender', _('Agender')
#         PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')
#
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="profile",
#         help_text="The associated Django User"
#     )
#     display_name = models.CharField(max_length=128, blank=True, null=True)
#     gender = models.CharField(max_length=32, choices=Gender.choices, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     birthdate = models.DateField(blank=True, null=True)
#     phone = PhoneNumberField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ["display_name"]
#         verbose_name = _("profile")
#         verbose_name_plural = _("profiles")
