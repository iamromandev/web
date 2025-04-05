# Generated by Django 4.1.9 on 2025-04-05 14:23

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, choices=[('billing', 'Billing'), ('shipping', 'Shipping'), ('home', 'Home'), ('work', 'Work'), ('office', 'Office'), ('po_box', 'PO Box'), ('delivery', 'Delivery'), ('mailing', 'Mailing'), ('temporary', 'Temporary'), ('other', 'Other')], max_length=32, null=True)),
                ('address_line_1', models.CharField(max_length=256)),
                ('address_line_2', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coordinate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to='core.coordinate')),
                ('locations', models.ManyToManyField(blank=True, related_name='addresses', to='core.location')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'ordering': ['address_line_1'],
            },
        ),
    ]
