import uuid

from django.db import models

from django_softdelete.models import SoftDeleteModel

from apps.core.models import Source, Language


# Create your models here.
class Todo(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    source = models.ForeignKey(Source, related_name="todo_todos", on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, related_name="todo_todos", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=128, blank=False, null=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f'[Todo: {self.title.encode("utf8")}]'
