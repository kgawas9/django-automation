"""
Import data functionality using csv file.
"""

from django.core.management.base import BaseCommand, CommandParser, CommandError

# from dataentry.models import Student
from django.apps import apps

import csv

class Command(BaseCommand):
    """Import data functionality for csv dataset."""

    help = "This functionality is related to importing data from csv file."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Required filepath to import the data.')
        parser.add_argument('model_name', type=str, help='Required model name to import the data.')

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

            # Search for models across all the installed apps
            model = None
            for app_config in apps.get_app_configs():

                model_name = kwargs['model_name'].capitalize()

                try:
                    model = apps.get_model(app_config.label, model_name)
                    break
                except LookupError:
                    continue
                    # self.stdout.write(self.style.WARNING(f"{app_config.label} - unable to look up {model_name}"))

            if not model:
                raise CommandError(f"Unable to find '{model_name}' in registered applications.")
                
            # insert all the rows into table
            try:
                [model.objects.create(**data) for data in reader]
            except Exception as e:
                raise LookupError(f"Unable to insert data into table {model_name}. {e}")

            # [
            #     kwargs['model_name'].objects.create(**data)
            #     if not Student.objects.filter(roll_no=data['roll_no']).exists()
            #     else self.stdout.write(self.style.WARNING(f"{data['roll_no']} already exists in DB."))
            #     for data in reader
            # ]

        self.stdout.write(self.style.SUCCESS(f'Data successfully imported from CSV to "{model_name}" model.'))
