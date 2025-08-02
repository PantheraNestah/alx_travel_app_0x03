from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample listings'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create some users
        users = []
        for i in range(5):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='password')
                users.append(user)
            else:
                users.append(User.objects.get(username=username))

        # Create some listings
        titles = ['Cozy Cottage', 'Modern Loft', 'Beachfront Villa', 'Mountain Cabin', 'Urban Apartment']
        for title in titles:
            if not Listing.objects.filter(title=title).exists():
                Listing.objects.create(
                    title=title,
                    description=f'A beautiful {title.lower()}.',
                    price=random.uniform(50.00, 500.00),
                    owner=random.choice(users)
                )
        
        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))