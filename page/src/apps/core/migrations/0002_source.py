# Generated by Django 4.1.9 on 2025-03-25 18:24

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=32)),
                ('subtype', models.CharField(max_length=32)),
                ('origin', models.CharField(max_length=32)),
                ('source', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
                'ordering': ['source'],
            },
        ),
    ]
