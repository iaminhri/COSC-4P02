# myapp/views.py
from pydoc_data.topics import topics

# import newspaper
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import UserPreference
from .forms import UserPreferenceForm
from .utils import fetch_articles_from_api_1
from django.db.models import Q
from UserPreferenceApp.models import Article, ArticleFrench
from rest_framework import viewsets
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from UserPreferenceApp.models import LikedBy

@login_required
def like_post(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        user = request.user

        try:
            article_french = article.french  
        except ArticleFrench.DoesNotExist:
            article_french = None

        # Check if already liked
        liked_obj = LikedBy.objects.filter(user=user, article=article).first()

        if liked_obj:
            # Unlike 
            liked_obj.delete()
        else:
            # Like 
            LikedBy.objects.create(
                user=user,
                article=article,
                article_french=article_french  
            )

        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required
def preferences(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_pref, created = UserPreference.objects.get_or_create(user=request.user)
        
        if request.method == "POST":

            form = UserPreferenceForm(request.POST, instance=user_pref)

            if form.is_valid():
                form.save()
                messages.success(request, "Preferences Saved Successfully!")
        else:    
            if user_pref: 
                form = UserPreferenceForm(instance=user_pref)
            else:
                form = UserPreferenceForm()

        return render(request, 'set_preferences.html', {'form': form})

@login_required
def aggregate_content(request):
    topics = ["AI", "Quantum Computing"]
    keywords = ["Technology"]

    articles = fetch_articles_from_api_1(topics, keywords)
    return render(request, 'news_results.html', {"articles": articles})

@login_required
def user_contents(request):
    preferences, _ = UserPreference.objects.get_or_create(user=request.user)
    
    topics = preferences.topics
    keywords = preferences.keywords

    contents = check_articles(topics, keywords)

    paginator = Paginator(contents, 8)
    pageNumber = request.GET.get('p', 1)
    articlePageObj = paginator.get_page(pageNumber)
    
    return render(request, 'users/user_contents.html', {'articles': articlePageObj})

def check_articles(topics, keywords):
    topics_list = [topic.strip() for topic in topics.split(',') if topic.strip()]
    keywords_list = [keyword.strip() for keyword in keywords.split(',') if keyword.strip()]
    
    query = Q()
    for term in topics_list + keywords_list:
        query |= Q(title__icontains=term) | Q(description__icontains=term)
    
    existingArticles = Article.objects.filter(query)

    if existingArticles.exists():
        articles_list = list(existingArticles)
        return articles_list
    else:
        print("No articles found.")
        return []

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

class TypeViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.all()
        topic = self.request.query_params.get('topic')
        keyword = self.request.query_params.get('keyword') 

        if topic:
            queryset = queryset.filter(topic__iexact=topic)
        if keyword:
            queryset = queryset.filter(keyword__icontains=keyword)

        return queryset