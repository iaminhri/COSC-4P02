from django.shortcuts import render
from django.http import HttpResponse

from .models import Preferences

def index(request):
    return HttpResponse("Welcome to the AI-Powered News Platform!")

# Scrum 2 task 1&2: Create input fields for sources, topics, and keywords & Implement a database to store user preferences.
def preferences(request):
    if request.method == "POST":
        # Get data
        sources = request.POST.get('sources')
        topics = request.POST.get('topics')
        keywords = request.POST.get('keywords')

        # Save data to database
        Preferences.objects.create(sources=sources, topics=topics, keywords=keywords)

        return HttpResponse("Preferences saved successfully!")

    return render(request, 'preferences.html')

# Scrum 3 task1: Generate email template
def email_template_1(request):
    return render(request, 'email_template_1.html')
def email_template_2(request):
    return render(request, 'email_template_2.html')
def email_template_3(request):
    return render(request, 'email_template_3.html')


