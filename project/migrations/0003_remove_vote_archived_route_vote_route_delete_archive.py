# Generated by Django 5.1.3 on 2024-11-22 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_route_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='archived_route',
        ),
        migrations.AddField(
            model_name='vote',
            name='route',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='project.route'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Archive',
        ),
    ]
