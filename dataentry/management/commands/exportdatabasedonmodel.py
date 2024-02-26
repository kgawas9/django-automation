"""
Export the data based on user required datatable.
"""

from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.conf import settings

from django.apps import apps

from dataentry.utils import get_model
from datetime import datetime
import csv
import os


def get_default_directory_to_export_files():
    directory_name = 'export_data'

    export_dir_path = os.path.join(settings.BASE_DIR, directory_name)

    if not os.path.exists(export_dir_path):
        os.makedirs(export_dir_path)

    return export_dir_path

class Command(BaseCommand):
    """Import data to csv with given model details."""

    help = "Import data to csv with given datatable."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model_name', type=str, help="Provide model name to export the data.")
        parser.add_argument('file_path', type=str)


    def handle(self, *args, **kwargs):
        model = get_model(model_name=kwargs['model_name'])
        file_path = kwargs['file_path']
        
        if not model:
            raise CommandError(f"Unable to find table in database with name {kwargs['model_name']}.")


        # fetch data from model/table
        extract_data = model.objects.all()

        
        # download data
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)

            headers = [field.name for field in model._meta.get_fields()]
            writer.writerow(headers)

            for data in extract_data:
                row_data = [getattr(data, field.name) for field in model._meta.get_fields()]
                writer.writerow(row_data)

        self.stdout.write(self.style.SUCCESS(f"Data successfully downloaded for {kwargs['model_name']} table in {file_path} direcotry."))
