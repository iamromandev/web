# Generated by Django 4.1.9 on 2025-04-05 14:22

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Coordinate',
                'verbose_name_plural': 'Coordinates',
                'ordering': ('latitude', 'longitude'),
                'unique_together': {('latitude', 'longitude')},
            },
        ),
    ]
