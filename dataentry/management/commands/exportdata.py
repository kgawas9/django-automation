"""
Create a comamnd to export data from database tables to csv.
"""

from django.core.management.base import BaseCommand
from django.conf import settings

from dataentry.models import Student

from datetime import datetime
import csv
import os


def default_folder_to_export_data():
    directory_name = "export_data"

    export_data_dir = os.path.join(settings.BASE_DIR, directory_name)

    if not os.path.exists(export_data_dir):
        os.makedirs(export_data_dir)

    return export_data_dir

class Command(BaseCommand):
    """export the data from table to csv."""

    help = "Export the data form student table to csv."

    def handle(self, *args, **kwargs):
        # fetch the data from Student database table

        export_directory = default_folder_to_export_data()
        student_data = Student.objects.all()
        
        # define the csv file
        file_path = f'{export_directory}\student-data-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")}.csv'
        
        # Open the file and write the data
        with open(file_path, 'w', newline="") as file:
            writer = csv.writer(file)
            
            # write the csv header
            writer.writerow(['Id', 'Roll no', 'Name', 'Age'])

            # write data rows
            # for student in student_data:
                # writer.writerow([student.id, student.roll_no, student.name, student.age])

            [writer.writerow([student.id, student.roll_no, student.name, student.age]) for student in student_data]

        self.stdout.write(self.style.SUCCESS(f"Data successfully exported to {file_path} location."))

        