import uuid

from django.db import models

from django_softdelete.models import SoftDeleteModel


# Create your models here.

class Lake(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ref = models.TextField(blank=False, null=False)
    extra = models.TextField(blank=True, null=True)
    raw = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f'[Lake: {self.ref}] update_at: {self.updated_at}'
