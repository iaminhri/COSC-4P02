from django.shortcuts import render
from django.http import HttpResponse 
from UserPreferenceApp.utils import fetch_articles_from_api_3 as fetchArticles
from django.core.paginator import Paginator
from UserPreferenceApp.models import Article 
from django.db.models import Q


def home(request):
    # topics = ["Science", "Computer Science", "Health", "Education", "Politics", "Environment"]
    # keywords = ["AI", "Blockchain"]

    # topics_and_keywords = {
    #     "Science": ["Experiment", "Theory"],
    #     "Technology": ["Innovation", "Gadgets"],
    #     "Health": ["Wellness", "Medicine"],
    #     "Education": ["Learning", "Schools"],
    #     "Environment": ["Conservation", "Climate"],
    #     "Computer Science": ["technology", "Artificial Intelligence", "AI", "Research", "University"]
    # }

    # topics_and_keywords = {
    #     "Arts": ["Painting", "Sculpture", "Photography"],
    #     "Business": ["Entrepreneurship", "Startups", "Mergers", "Acquisitions"],
    #     "Politics": ["Elections", "Legislation", "Diplomacy", "Policies"],
    #     "Sports": ["Football", "Basketball", "Olympics", "Tennis"],
    #     "Culture": ["Literature", "Cinema", "Traditions", "Festivals"],
    #     "Economics": ["Markets", "Stocks", "Trade", "Economic Growth"],
    #     "Psychology": ["Cognitive", "Behavioral", "Therapy", "Mental Health"],
    #     "Technology": ["Robotics", "Machine Learning", "Blockchain", "Cybersecurity"],
    #     "Environment": ["Renewable Energy", "Wildlife Conservation", "Climate Change"],
    #     "Food": ["Cuisine", "Recipes", "Nutrition", "Veganism"],
    #     "Travel": ["Destinations", "Adventure", "Cultural Experiences", "Travel Tips"],
    #     "Fashion": ["Trends", "Designers", "Runways", "Sustainable Fashion"]
    # }

    # for topics, keywords in topics_and_keywords.items():
    #     articles = fetchArticles(request.user, [topics], keywords)
        
    # articles = check_articles(request.user, topics, keywords)
    # articles = fetchArticles(request.user, topics, keywords)
    articles = fetch_all_articles()
    
    paginator = Paginator(articles, 8)
    pageNumber = request.GET.get('p', 1)
    articlePageObj = paginator.get_page(pageNumber)

    return render(request, 'home.html', {"articles": articlePageObj})

def fetch_all_articles():
    all_articles = Article.objects.all()
    return all_articles

def check_articles(user, topics, keywords):
    print("Topics:", topics)
    print("Keywords:", keywords)
    print("Combined Search:", topics + keywords)

    # Creating a Q object for complex queries
    query = Q()
    for term in topics + keywords:
        query |= Q(title__icontains=term) | Q(description__icontains=term)  # Search both title and description
    
    existingArticles = Article.objects.filter(query, user=user)
    print("SQL Query:", existingArticles.query)  # Outputs the SQL query

    if existingArticles.exists():
        articles_list = list(existingArticles)
        print("Found Articles:", articles_list)
        return articles_list
    else:
        print("No articles found.")
        return []