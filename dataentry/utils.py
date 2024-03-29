from django.apps import apps
from django.core.management.base import CommandError
from django.core.mail import EmailMessage
from django.db import DataError
from django.conf import settings

import os
import csv
from datetime import datetime


def get_custom_models():

    # Apps to exclude
    EXCLUDE_APPS = ['auth', 'contenttypes', 'sessions', 'admin']
    # EXCLUDE_APPS = ['admin.logentry']

    all_models = apps.get_models()
    
    # custom_models = [model._meta.label for model in all_models if model._meta.label.lower() not in EXCLUDE_APPS]
    custom_models = [model.__name__ for model in all_models if model._meta.app_label not in EXCLUDE_APPS]

    return custom_models


def check_upload_csv_errors(filepath, model_name):
    
    model = None
    for app_config in apps.get_app_configs():

        model_name = model_name.capitalize()
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue
            # self.stdout.write(self.style.WARNING(f"{app_config.label} - unable to look up {model_name}"))
    
    if not model:
        file.close()
        os.remove(path=filepath)
        raise CommandError(f"Unable to find '{model_name}' in registered applications.")
        
    # get model field name
    model_fields = [field.name for field in model._meta.fields if not field.name == 'id']


    # compare csv header with model field names
    try:
        with open(filepath, "r") as file:
            # returns DictReader object
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            if csv_header != model_fields:
                file.close()
                os.remove(path=filepath)
                raise DataError(f"Headers of CSV file doesn't match with '{model.__name__}' table fields.")
            
    except Exception as e:
        raise e
    
    return model



def send_email_communication(email_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        mail = EmailMessage(email_subject, message, from_email, to_email)
        
        print(attachment)
        
        if attachment:
            print(attachment)
            mail.attach_file(attachment)

        mail.send()
    except Exception as e:
        raise e



def get_model(model_name):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name.capitalize())
            # print(model.__name__)
            break
        except Exception as e:
            continue

    return model


def get_default_directory_to_export_files():
    directory_name = 'export_data'

    export_dir_path = os.path.join(settings.MEDIA_ROOT, directory_name)

    if not os.path.exists(export_dir_path):
        os.makedirs(export_dir_path)

    return export_dir_path


def get_directory_path(model_name):
    directory_path = get_default_directory_to_export_files()
    file_path = os.path.join(settings.BASE_DIR, f"{directory_path}\{model_name.lower()}-data-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.csv")

    return file_path