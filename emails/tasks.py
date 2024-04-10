from django.conf import settings

from automation_project.celery import app
from dataentry.utils import send_email_communication


@app.task
def send_email_to_list(subject, message, to, attachment=None):
    try:
        send_email_communication(email_subject=subject, message=message, to_email=to, attachment=attachment)

        email_subject = f"Email with subject line - {subject}"
        message = "Email successfully sent to the list of users."
        to_email = ['usetmp1@gmail.com']
        
        send_email_communication(email_subject, message, to_email)
        return 'Task executed successfully.'
    
    except Exception as e:
        raise e
