# Generated by Django 5.1.3 on 2024-12-09 22:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0006_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mini_fb_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
