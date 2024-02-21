from django.contrib import admin
from .models import Student, Customer, Employee

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'roll_no', 'name', 'age'
    ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'country'
    ]


admin.site.register(Employee)