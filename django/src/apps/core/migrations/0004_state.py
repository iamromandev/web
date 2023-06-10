# Generated by Django 4.1.9 on 2023-06-04 15:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref', models.UUIDField()),
                ('state', models.CharField(max_length=32)),
                ('extra', models.CharField(blank=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='states', to='core.source')),
            ],
            options={
                'ordering': ['source'],
                'unique_together': {('ref', 'source')},
            },
        ),
    ]