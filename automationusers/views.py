from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .forms import RegistrationForm


# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration completed.")
            return redirect('register')
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



def login_user(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            
            if not user:
                messages.error(request, 'User not found, please check the credentials.')
                return redirect('login')
            
            login(request, user=user)
            messages.success(request, 'Authentication successful.')
            return redirect('home')
        else:
            messages.error(request, f'Invalid credentials. {login_form.error_messages} ')
            return redirect('login')


    form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'automationusers/login.html', context=context)



def logout_user(request):
    logout(request)
    messages.success(request, 'User successfully logged out.')
    return redirect('login')
