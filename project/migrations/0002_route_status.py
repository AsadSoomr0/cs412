# Generated by Django 5.1.3 on 2024-11-22 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='status',
            field=models.CharField(choices=[('current', 'Current'), ('archived', 'Archived')], default='current', max_length=10),
        ),
    ]