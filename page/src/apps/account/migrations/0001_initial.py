# Generated by Django 4.1.9 on 2025-04-13 18:29

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0010_platform'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPlatform',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('youtube', 'YouTube'), ('whatsapp', 'WhatsApp'), ('instagram', 'Instagram'), ('tiktok', 'TikTok'), ('wechat', 'WeChat'), ('facebook_messenger', 'Facebook Messenger'), ('telegram', 'Telegram'), ('twitter', 'X (formerly Twitter)'), ('snapchat', 'Snapchat'), ('pinterest', 'Pinterest'), ('linkedin', 'LinkedIn'), ('reddit', 'Reddit'), ('discord', 'Discord'), ('tumblr', 'Tumblr'), ('threads', 'Threads'), ('bluesky', 'Bluesky'), ('mastodon', 'Mastodon'), ('other', 'Other')], max_length=32, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('platform', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_platform', to='core.platform')),
            ],
            options={
                'verbose_name': 'Social Platform',
                'verbose_name_plural': 'Social Platforms',
                'ordering': ['platform__name'],
            },
        ),
    ]
