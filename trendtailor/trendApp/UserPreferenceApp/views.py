# myapp/views.py
from pydoc_data.topics import topics

# import newspaper
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserPreference
from .forms import UserPreferenceForm
from .utils import fetch_articles_from_api


def preferences_success(request):
    return render(request, 'preferences_success.html')

@login_required
def fetch_news_view(request):
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


@login_required
def set_preferences_view(request):
    # Try to get existing preferences or create a blank record
    preference, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('preferences_success')  # or wherever you want
    else:
        form = UserPreferenceForm(instance=preference)

    return render(request, 'set_preferences.html', {'form': form})


def preferences(request):
    if request.method == "POST":
        sources = request.POST.get('sources')
        topics = request.POST.get('topics')
        keywords = request.POST.get('keywords')

        UserPreference.objects.create(sources=sources, topics=topics, keywords=keywords)

        return HttpResponse("Preferences saved successfully!")

    return render(request, 'set_preferences.html')


def aggregate_content(request):
    topics = ["AI", "Quantum Computing"]
    keywords = ["Technology"]

    articles = fetch_articles_from_api(topics, keywords)

    return render(request, 'news_results.html', {"articles": articles})

