from django.apps import apps


def get_custom_models():

    # Apps to exclude
    EXCLUDE_APPS = ['auth', 'contenttypes', 'sessions', 'admin']
    # EXCLUDE_APPS = ['admin.logentry']

    all_models = apps.get_models()
    
    # custom_models = [model._meta.label for model in all_models if model._meta.label.lower() not in EXCLUDE_APPS]
    custom_models = [model.__name__ for model in all_models if model._meta.app_label not in EXCLUDE_APPS]

    return custom_models


