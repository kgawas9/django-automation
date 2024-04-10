from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .models import EmailList
from .forms import EmailForm
from dataentry.utils import send_email_communication

from .tasks import send_email_to_list

# Create your views here.

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
     
        if email_form.is_valid():
            # send an email
            email_form = email_form.save()

            subscriber_list = EmailList.objects.get(id=request.POST.get('email_list')).subscriber_set.all()

            # to get the email list name from form
            # form = email_form.save()
            # print(email_form.email_list)
            
            to_email_list = [email.email_address for email in subscriber_list]
            email_subject = request.POST.get('subject')
            email_body = request.POST.get('body')

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # attachment_path = os.path.join(settings.MEDIA_ROOT, 'email_attachments', attachment_file.name)
            # print(attachment_path)
            # with open(attachment_path, 'wb') as destination:
            #     for chunk in attachment_file.chunks():
            #         destination.write(chunk)

            # send_email_communication(email_subject=email_subject, message=email_body, to_email=to_email_list, attachment=attachment)

            # using celery
            send_email_to_list.delay(subject=email_subject, message=email_body, to=to_email_list, attachment=attachment)

            messages.success(request, 'Your emails are being sent, you will be notified once its done.')
            return redirect('send-email')
        
    email_form = EmailForm()
    context = {
        'form': email_form,
    }
    return render(request, 'emails/send-email.html', context=context)
