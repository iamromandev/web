# Generated by Django 4.1.9 on 2023-06-04 16:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_state'),
        ('dictionary', '0006_example'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('relation_type', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='dictionary_relation_types', to='core.source')),
            ],
            options={
                'ordering': ['relation_type'],
            },
        ),
    ]
