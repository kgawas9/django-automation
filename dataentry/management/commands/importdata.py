"""
Import data functionality using csv file.
"""

from django.core.management.base import BaseCommand, CommandParser

from dataentry.models import Student

import csv

class Command(BaseCommand):
    """Import data functionality for csv dataset."""

    help = "This functionality is related to importing data from csv file."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Required filepath to import the data.')

    def handle(self, *args, **kwargs):
        """Create and update data in database using csv file."""
        self.stdout.write(f'{kwargs.get("file_path", "")}')

        with open(kwargs['file_path'], "r") as file:
            # returns DictReader object
            reader = csv.DictReader(file)
            
            # Insert data using list comprehension
            # [Student.objects.create(roll_no = data['roll_no'], name=data['name'], age=data['age']) for data in reader if not Student.objects.filter(roll_no=data['roll_no']).exists()]

            # [
            #     Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            #     if not Student.objects.filter(roll_no=data['roll_no']).exists()
            #     else self.stdout.write(self.style.WARNING(f"{data['roll_no']} already exists in DB."))
            #     for data in reader
            # ]

            [
                Student.objects.create(**data)
                if not Student.objects.filter(roll_no=data['roll_no']).exists()
                else self.stdout.write(self.style.WARNING(f"{data['roll_no']} already exists in DB."))
                for data in reader
            ]

        self.stdout.write(self.style.SUCCESS('Data successfully imported from CSV.'))
