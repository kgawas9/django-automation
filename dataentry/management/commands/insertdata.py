"""
Add some data to the database using custom command.
"""

from django.core.management.base import BaseCommand, CommandParser
from dataentry.models import Student

from faker import Faker
from typing import Any

import random


# Initialize Faker
fake = Faker()

# Generate fake roll numbers, names, and ages
def generate_fake_data(num_entries):
    data = []
    for _ in range(num_entries):
        roll_no = str(fake.random_int(min=1001, max=9999))  # Generate a 4-digit random roll number
        name = fake.name()
        age = random.randint(18, 40)  # Generate a random age between 18 and 30
        data.append({'roll_no': roll_no, 'name': name, 'age': age})
    return data


class Command(BaseCommand):
    """Insert data to database."""

    help = "Custom command to insert data to database."

    def add_arguments(self, *args, **kwargs):
        pass
    
    def handle(self, *args: Any, **options: Any):
        # business logic

        # create single entry
        # student = Student.objects.create(
        #     roll_no='1001', name='Kiran Gawas', age=32
        # )

        # create multiple entries using faker library
        self.stdout.write('Insert data process initiated, please wait....')
        data = generate_fake_data(100)

        for record in data:

            if not Student.objects.filter(roll_no = record['roll_no']).exists():
                Student.objects.create(
                    roll_no = record['roll_no'],
                    name = record['name'],
                    age = record['age']
                )
            else:
                self.stdout.write(self.style.WARNING(f'Record with roll_no {record["roll_no"]} already exist in database.'))

        self.stdout.write(self.style.SUCCESS(f'student(s) data successfully inserted.'))
