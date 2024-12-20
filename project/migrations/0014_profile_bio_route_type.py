# Generated by Django 5.1.3 on 2024-12-10 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_profile_completed_routes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='type',
            field=models.CharField(choices=[('overhang', 'Overhang'), ('slab', 'Slab'), ('vertical', 'Vertical'), ('traverse', 'Traverse'), ('dyno', 'Dyno')], default='overhang', max_length=20),
        ),
    ]
