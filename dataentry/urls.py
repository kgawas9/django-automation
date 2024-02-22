from django.urls import path

from . import views

urlpatterns = [
    path('import-data/', views.import_data, name='import-data'),
    path('celery-test/', views.celery_test, name='celery-test')
]