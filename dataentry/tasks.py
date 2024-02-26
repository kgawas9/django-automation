from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings

from uploads.models import Upload
from automation_project.celery import app

from .utils import send_email_communication, get_directory_path

import time


@app.task
def celery_test_task():
    time.sleep(10)
    try:
        email_subject = "Test email"
        message = "This is test email to check the email functionality."
        to_email = ['usetmp1@gmail.com']

        send_email_communication(email_subject, message, to_email)

    except Exception as e:
        raise e

    return 'Task executed successfully.'


@app.task
def import_data_task(upload_id, file_path, model_name):

    to_email = ['usetmp1@gmail.com']

    try:
        call_command('importdata', file_path, model_name)
        email_subject = "Data Import Task completed."
        message = "Data successfully imported to database."
        send_email_communication(email_subject, message, to_email)

    except Exception as e:
        email_subject = "Data Import Task completed."
        message = f"Failed to import data to database. {e}"
        send_email_communication(email_subject, message, to_email)

        upload = Upload.objects.get(pk=upload_id)
        Upload.objects.get(file=upload.file).delete()
        raise e
    
    return 'Data successfully imported.'



@app.task
def export_model_data(model_name):
    try:
        file_path = get_directory_path(model_name)
        call_command('exportdatabasedonmodel', model_name, file_path)
    
    except Exception as e:
        raise e
    
    # Send email with attachment


    email_subject = f"data exported successfully for {model_name} model"
    message = f"Export data successful. Please find the attached file."
    to_email = ['kgawas9@gmail.com']
    send_email_communication(email_subject, message=message, to_email=to_email, attachment=file_path)

    return 'Export data task executed successfully.'
