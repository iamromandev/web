# Generated by Django 4.1.9 on 2023-05-24 04:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=8)),
                ('origin', models.CharField(blank=True, max_length=32, null=True)),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('direction', models.CharField(blank=True, choices=[('LTR', 'left-to-right'), ('RTL', 'right-to-left')], default=None, max_length=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='languages', to='core.source')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
