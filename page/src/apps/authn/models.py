import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel

from apps.core.models import Code, User


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

    @property
    def is_verified(self) -> bool:
        return self.status == Verification.Status.VERIFIED
