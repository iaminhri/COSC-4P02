from django.shortcuts import render
from django.http import HttpResponse

#from .models import UserPreference

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')


# myapp/views.py
from django.shortcuts import render
