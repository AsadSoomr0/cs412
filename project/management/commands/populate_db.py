from django.core.management.base import BaseCommand
from project.models import Route
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with dummy data for Routes"

    def handle(self, *args, **kwargs):
        # Clear existing routes
        Route.objects.all().delete()

        # Define static data for types and statuses
        route_types = [choice[0] for choice in Route.TYPE_CHOICES]
        statuses = ['current', 'archived']

        # Create 15 current routes and 10 archived routes
        for i in range(25):
            route_type = random.choice(route_types)
            difficulty = random.randint(0, 12)  # Difficulty corresponds to V0-V12
            status = 'current' if i < 15 else 'archived'
            date_set = fake.date_this_year()
            replacement_date = date_set + timedelta(days=random.randint(30, 60))

            Route.objects.create(
                name=fake.word().capitalize(),
                type=route_type,
                difficulty=difficulty,  # Store the integer (e.g., 3 for V3)
                location=random.choice(['Main Building', 'Annex']),
                setter_name=fake.name(),
                date_set=date_set,
                replacement_date=replacement_date,
                status=status,
                image=None,
            )

        self.stdout.write(self.style.SUCCESS("Database populated with 25 routes (15 current, 10 archived)."))
