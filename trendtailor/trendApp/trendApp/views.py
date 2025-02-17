from django.shortcuts import render
from django.http import HttpResponse 
from UserPreferenceApp.utils import fetch_articles_from_api_1, fetch_articles_from_api_3
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 
from django.db.models import Q


def home(request):
    topics_and_keywords = {
        "Artificial": ["Artificial", "Artificial", "Intelligence", "AI", "Research", "University", "Medical", "Stock", "Market"],
        "technology": ["web", "development", "softwares", "Blockchain", "Cyber Security", "Internet of Things", "Machine Learning"],        "Science": ["Experiment", "Theory"],
        "Technology": ["Innovation", "Gadgets"],
        "Health": ["Wellness", "Medicine"],
        "Education": ["Learning", "Schools"],
        "Environment": ["Conservation", "Climate"],
        "Arts": ["Painting", "Sculpture", "Photography"],
        "Business": ["Entrepreneurship", "Startups", "Mergers", "Acquisitions"],
        "Politics": ["Elections", "Legislation", "Diplomacy", "Policies"],
        "Sports": ["Football", "Basketball", "Olympics", "Tennis"],
        "Culture": ["Literature", "Cinema", "Traditions", "Festivals"],
        "Economics": ["Markets", "Stocks", "Trade", "Economic Growth"],
        "Psychology": ["Cognitive", "Behavioral", "Therapy", "Mental Health"],
        "Technology": ["Robotics", "Machine Learning", "Blockchain", "Cybersecurity"],
        "Environment": ["Renewable Energy", "Wildlife Conservation", "Climate Change"],
        "Food": ["Cuisine", "Recipes", "Nutrition", "Veganism"],
        "Travel": ["Destinations", "Adventure", "Cultural Experiences", "Travel Tips"],
        "Fashion": ["Trends", "Designers", "Runways", "Sustainable Fashion"]
    }

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_1([topics], keywords)

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_2([topics], keywords)

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetch_articles_from_api_3([topics], keywords)   

    articles = fetch_all_articles()

    print("Max Number of Pages", len(articles) / 50)
    
    paginator = Paginator(articles, 52)
    pageNumber = request.GET.get('p', 1)
    articlePageObj = paginator.get_page(pageNumber)

    return render(request, 'home.html', {"articles": articlePageObj})

def fetch_all_articles():
    all_articles = Article.objects.all()
    return all_articles

def check_articles(user, topics, keywords):    
    query = Q()
    # Assuming topics and keywords are lists
    for term in topics + keywords:
        query |= Q(title__icontains=term) | Q(description__icontains=term)
    
    existingArticles = Article.objects.filter(query)

    if existingArticles.exists():
        articles_list = list(existingArticles)
        return articles_list
    else:
        return []

# Scrum 3 task1: Generate email template
def email_template_1(request):
    return render(request, 'email_template_1.html')
def email_template_2(request):
    return render(request, 'email_template_2.html')
def email_template_3(request):
    return render(request, 'email_template_3.html')

