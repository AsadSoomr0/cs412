# Generated by Django 5.1.3 on 2024-12-09 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_newsletterpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletterpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='newsletter_images/'),
        ),
        migrations.AlterField(
            model_name='newsletterpost',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
