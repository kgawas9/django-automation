from django.shortcuts import render, redirect
from django.conf import settings
from django.apps import apps
from django.core.management import call_command

from .utils import get_custom_models
from uploads.models import Upload

import os
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


            # trigger the importdata command
            try:
                call_command('importdata', file_path, model_name)
            except Exception as e:
                raise e

            return redirect('import-data')
        
        else:
            raise ValueError('File or model name not selected.')
    
    custom_models = get_custom_models()

    context = {
        'custom_models': custom_models
    }

    return render(request, 'dataentry/importdata.html', context=context)
