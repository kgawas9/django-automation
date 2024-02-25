from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.apps import apps
from django.core.management import call_command
from django.contrib import messages

from .utils import get_custom_models, check_upload_csv_errors, get_model
from uploads.models import Upload

import os
import time
from .tasks import celery_test_task, import_data_task, export_model_data
# Create your views here.


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        if file_path and model_name:
            # store the file inside upload model
            upload = Upload.objects.create(
                                file=file_path, model_name=model_name
                            )
            # construct full path (relative path)
            relative_path = str(upload.file.url)

            base_dir = str(settings.BASE_DIR)
            file_path = base_dir + relative_path

            # check for any potential error in csv
            try:
                model = check_upload_csv_errors(filepath=file_path, model_name=model_name)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('import-data')

            # trigger the importdata command
            import_data_task.delay(upload_id=upload.id, file_path=file_path, model_name=model_name)

            messages.success(request, 'Your data is being imported, you will be notified once its done.')
            return redirect('import-data')
        
        else:
            messages.error(request, f"File or model name not selected.")
            return redirect('import-data')
    
    custom_models = get_custom_models()

    context = {
        'custom_models': custom_models
    }

    return render(request, 'dataentry/importdata.html', context=context)



def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get('model_name')

        model = get_model(model_name=model_name)

        if not model:
            messages.error(request, "Unable to export data. Contact your administrator.")
            return redirect('export-data')
        
        export_model_data.delay(model_name)

        messages.success(request, f"Data from '{model_name}' table is being exported. You will be notified once it's done.")
        return redirect('export-data')

    models = get_custom_models()
    context = {
        'custom_models': models
    }

    return render(request, 'dataentry/exportdata.html', context=context)

def celery_test(request):
    # Execute the celery task
    celery_test_task.delay()
    
    return HttpResponse('<h4>Function successfully executed</h4>')
