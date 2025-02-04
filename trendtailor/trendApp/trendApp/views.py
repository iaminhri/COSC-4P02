from django.shortcuts import render
from django.http import HttpResponse

#from .models import UserPreference

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')


# myapp/views.py
from django.shortcuts import render
from .utils import fetch_articles_from_api


def aggregate_content(request):
    topics = ["AI", "Quantum Computing"]
    keywords = ["Technology"]

    articles = fetch_articles_from_api(topics, keywords)

    return render(request, 'news_results.html', {"articles": articles})
