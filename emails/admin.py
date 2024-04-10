from django.contrib import admin
from .models import EmailList, Subscriber, Email

# Register your models here.

@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'email_list'
    ]


@admin.register(Subscriber)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'email_address'
    ]


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'subject'
    ]