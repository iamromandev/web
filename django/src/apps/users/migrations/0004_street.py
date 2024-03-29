# Generated by Django 4.1.9 on 2023-06-20 12:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_state'),
        ('users', '0003_locality'),
    ]

    operations = [
        migrations.CreateModel(
            name='Street',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.CharField(blank=True, max_length=32, null=True)),
                ('route', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_streets', to='core.source')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
    ]
