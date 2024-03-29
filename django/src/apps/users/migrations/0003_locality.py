# Generated by Django 4.1.9 on 2023-06-20 12:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_state'),
        ('users', '0002_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=16, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_localities', to='core.source')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='localities', to='users.state')),
            ],
            options={
                'ordering': ('state', 'name'),
            },
        ),
    ]
