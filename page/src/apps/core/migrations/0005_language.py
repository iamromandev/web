# Generated by Django 4.1.9 on 2025-04-06 16:40

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('native_name', models.CharField(blank=True, max_length=128, null=True)),
                ('direction', models.CharField(choices=[('ltr', 'Left to Right'), ('rtl', 'Right to Left')], default='ltr', max_length=3)),
                ('script', models.CharField(blank=True, choices=[('latin', 'Latin'), ('cyrillic', 'Cyrillic'), ('arabic', 'Arabic'), ('devanagari', 'Devanagari'), ('chinese', 'Chinese'), ('greek', 'Greek'), ('hebrew', 'Hebrew'), ('japanese', 'Japanese'), ('korean', 'Korean'), ('thai', 'Thai'), ('tamil', 'Tamil'), ('bengali', 'Bengali'), ('braille', 'Braille'), ('ethiopic', 'Ethiopic'), ('georgian', 'Georgian'), ('mongolian', 'Mongolian'), ('syriac', 'Syriac'), ('other', 'Other')], max_length=32, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('codes', models.ManyToManyField(blank=True, related_name='languages', to='core.code')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ['name'],
            },
        ),
    ]
