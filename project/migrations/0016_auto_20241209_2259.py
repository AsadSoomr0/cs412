from django.db import migrations, models

def populate_route_difficulties(apps, schema_editor):
    Route = apps.get_model('project', 'Route')

    for route in Route.objects.all():
        if route.difficulty in [None, '']:
            route.difficulty = 'V0' 
            route.save()

class Migration(migrations.Migration):
    dependencies = [
        ('project', '0015_remove_profile_membership_start_date_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_route_difficulties),
    ]
