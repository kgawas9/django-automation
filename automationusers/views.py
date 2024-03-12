from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm

# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed.")
            return redirect('/')
        else:
            context = {
                'form': form
            }
            return render(request, 'automationusers/register.html', context=context)
        
    user_form = RegistrationForm()

    context = {
        'form': user_form
    }
    return render(request, 'automationusers/register.html', context=context)
