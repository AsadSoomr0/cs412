# Generated by Django 5.1.2 on 2024-11-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='dob',
        ),
        migrations.AddField(
            model_name='voter',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='voter',
            name='voter_id',
            field=models.CharField(default='UNKNOWN', max_length=100),
        ),
        migrations.AlterField(
            model_name='voter',
            name='party_affiliation',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='voter',
            name='street_number',
            field=models.CharField(default=-1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='voter',
            name='v20state',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v21primary',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v21town',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v22general',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v23town',
            field=models.BooleanField(),
        ),
    ]
