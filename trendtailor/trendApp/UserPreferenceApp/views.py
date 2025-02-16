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
from UserPreferenceApp.models import Article 

# def preferences_success(request):
#     return render(request, 'preferences_success.html')

"""def fetch_news_view(request):
    try:
        user_pref = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        sources = ['https://www.cnn.com','https://www.bbc.com']
        topics = []
        keywords = []
    else:
        sources = user_pref.get_sources_list()
        topics = user_pref.get_topics_list()
        keywords = user_pref.get_keywords_list()

    filter_terms = [term.lower() for term in (topics + keywords)]
    relevant_articles = []

    for source in sources:
        try:
            paper = newspaper.build(source, memoize_articles=False)
        except Exception as e:
            print(f"Error accessing {source}: {e}")
            continue

        for article in paper.articles:
            try:
                article.download()
                article.parse()
            except Exception as e:
                print(f"Error parsing article {article.url}: {e}")
                continue

            title = article.title.lower() if article.title else ''
            content = article.text.lower()
            if any(term in title or term in content for term in filter_terms):
                relevant_articles.append({
                    'title':article.title,
                    'url': article.url,
                    'summary': article.text[:200]
                })

    return render(request, 'news_results.html', {'articles' : relevant_articles})

"""

# @login_required
# def set_preferences_view(request):
#     # Try to get existing preferences or create a blank record
#     preference, created = UserPreference.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = UserPreferenceForm(request.POST, instance=preference)
#         if form.is_valid():
#             form.save()
#             return redirect('preferences_success')  # or wherever you want
#     else:
#         form = UserPreferenceForm(instance=preference)

#     return render(request, 'set_preferences.html', {'form': form})

# def preferences(request):
#     if request.method == "POST":
#         sources = request.POST.get('sources')
#         topics = request.POST.get('topics')
#         keywords = request.POST.get('keywords')

#         UserPreference.objects.create(sources=sources, topics=topics, keywords=keywords)

#         messages.success(request, f'Preferences Saved Successfully !!!')
#         redirect('preferences')

#     return render(request, 'set_preferences.html')

@login_required
def preferences(request):
    # Try to retrieve existing preferences if they exist
    try:
        user_pref = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_pref = None
    
    if request.method == "POST":
        form = UserPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            user_pref = form.save(commit=False)
            user_pref.user = request.user  
            user_pref.save()
            messages.success(request, "Preferences Saved Successfully!")
            return redirect('preferences')
    else:
        if user_pref:
            form = UserPreferenceForm(instance=user_pref)
        else:
            form = UserPreferenceForm()

    return render(request, 'set_preferences.html', {'form': form})

def aggregate_content(request):
    topics = ["AI", "Quantum Computing"]
    keywords = ["Technology"]

    articles = fetch_articles_from_api_1(topics, keywords)
    return render(request, 'news_results.html', {"articles": articles})

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

    print("Length: ", len(existingArticles))

    if existingArticles.exists():
        articles_list = list(existingArticles)
        return articles_list
    else:
        print("No articles found.")
        return []