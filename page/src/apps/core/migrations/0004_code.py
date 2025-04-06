# Generated by Django 4.1.9 on 2025-04-06 16:39

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, choices=[('region', 'Region Code'), ('country', 'Country Code'), ('state_province', 'State/Province Code'), ('city', 'City Code'), ('status', 'Status Code'), ('error', 'Error Code'), ('product', 'Product Code'), ('order', 'Order Code'), ('shipping', 'Shipping Code'), ('payment', 'Payment Code'), ('currency', 'Currency Code'), ('language', 'Language Code'), ('priority', 'Priority Code'), ('role', 'Role Code'), ('category', 'Category Code'), ('event', 'Event Code'), ('license', 'License Code'), ('discount', 'Discount Code'), ('tax', 'Tax Code'), ('color', 'Color Code'), ('postal', 'Postal Code'), ('internal', 'Internal Code'), ('iso_alpha2', 'ISO 3166-1 Alpha-2'), ('iso_alpha3', 'ISO 3166-1 Alpha-3'), ('iso_numeric', 'ISO 3166-1 Numeric'), ('iso_3166_2', 'ISO 3166-2'), ('iso_639_1', 'ISO 639-1 Language'), ('iso_4217', 'ISO 4217 Currency'), ('iso_8601', 'ISO 8601 Date/Time'), ('iso_15924', 'ISO 15924 Script'), ('other', 'Other Code')], max_length=32, null=True)),
                ('code', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Code',
                'verbose_name_plural': 'Codes',
                'ordering': ['code'],
            },
        ),
    ]
