import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, User
from apps.media.models import Image


# Create your models here.
class Country(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="users_countries", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128, blank=True, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)


class State(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="users_states", on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, related_name="states", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=265, blank=True, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("country", "name")


class Locality(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="users_localities", on_delete=models.DO_NOTHING)
    state = models.ForeignKey(State, related_name="localities", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256, blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("state", "name")


class Street(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="users_streets", on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=32, blank=True, null=True)
    route = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("number",)


class Coordinate(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("latitude", "longitude")
        ordering = ("latitude", "longitude")


class Address(SoftDeleteModel):
    class Type(models.TextChoices):
        HOME = "HOME", _("home")
        WORK = "WORK", _("work")

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="users_addresses", on_delete=models.DO_NOTHING)
    street = models.ForeignKey(Street, related_name="addresses", on_delete=models.DO_NOTHING)
    locality = models.ForeignKey(Locality, related_name="addresses", on_delete=models.DO_NOTHING, blank=True, null=True)
    raw = models.CharField(max_length=256, blank=True, null=True)
    formatted = models.CharField(max_length=256, blank=True, null=True)
    coordinate = models.ForeignKey(Coordinate, related_name="addresses", on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=16, choices=Type.choices, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("locality", "street")


# class Profile(SoftDeleteModel):
#     class Gender(models.TextChoices):
#         MALE = "MALE", _("male")
#         FEMALE = "FEMALE", _("female")
#         OTHER = "OTHER", _("other")
#
#     id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
#     source = models.ForeignKey(Source, related_name="users_profiles", on_delete=models.DO_NOTHING)
#     user = models.ForeignKey(User, related_name="profiles", on_delete=models.DO_NOTHING)
#     #photo = models.OneToOneField(Image, on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to ='uploads/')
#     gender = models.CharField(max_length=16, choices=Gender.choices, default=None, blank=True, null=True)
#     birthday = models.DateField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ("user",)
