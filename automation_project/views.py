from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')  # Apply login_required decorator to the view
def home(request):
    return render(request, 'home.html')
