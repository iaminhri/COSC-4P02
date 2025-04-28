import requests
from django.conf import settings
from .models import Article 

def fetch_articles_from_api_1(topics, keywords):
    """Fetch articles using an external News API, filtered by topics/keywords."""
    api_key = getattr(settings,'NEWS_API_KEY',None)

    if not api_key:
        raise ValueError("API Key is not found")

    all_articles = []

    searchQuery = set(topics + keywords)

    for query in searchQuery:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                for article in articles:
                    new_article, created = Article.objects.get_or_create(
                        title=article['title'],
                        defaults={
                            'description': article['description'],
                            'contents': article.get('content', ''),
                            'url': article.get('url'),
                            'urlToImage': article.get('urlToImage'),
                            'topic': topics[0],
                            'keyword': keywords,
                        }
                    )
                    all_articles.append(new_article)
            else:
                return -1
        except requests.RequestException as e:
            all_articles.append(f"Error fetching articles for {query}: {str(e)}")

def fetch_articles_from_api_2(topics, keywords):
    api_key = getattr(settings, 'CURRENT_API_KEY',None)
    currents_url = "https://api.currentsapi.services/v1/search"

    if not api_key:
        raise ValueError("API Key is not found")
    
    all_articles = []

    searchQuery = set(topics + keywords)

    for query in searchQuery:
        params = {
            "apiKey": api_key,
            "q": query,
            "language": "en"
        }
        try:
            response = requests.get(currents_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # The Currents API returns articles under the "news" key.
                articles = data.get("news", [])
                for article in articles:
                    all_articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'url': article.get('url'), 
                            'urlToImage': article.get('image'),
                            'topic': topics[0],
                            'keyword': keywords,
                        })
            else:
                return -1
        except Exception as e:
            all_articles.append(f"Error fetching '{query}' from Currents API: {e}")
    
    return all_articles

def fetch_articles_from_api_3(topics, keywords):
    all_articles = []

    # existingArticles = Article.objects.filter(user=user, title__in=topics + keywords)
    # if existingArticles.exists():
    #     print(list(existingArticles))
    #     return list(existingArticles)

    gnews_api_key = getattr(settings, 'GNEWS_API_KEY', None)
    gnews_url = "https://gnews.io/api/v4/top-headlines"
    searchQuery = set(topics + keywords)

    for query in searchQuery:

        params = {
            "token": gnews_api_key,
            "q": query,
            "lang": "en",
            "max": 10  # maximum number of articles per request
        }
        try:
            response = requests.get(gnews_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()

                articles = data.get("articles", [])

                for article in articles:
                    new_article, created = Article.objects.get_or_create(
                        title=article['title'],
                        defaults={
                            'description': article['description'],
                            'contents': article.get('content', ''),
                            'url': article.get('url'),
                            'urlToImage': article.get('image'),
                            'topic': topics[0],
                            'keyword': keywords,
                        }
                    )
                    all_articles.append(new_article)
        except Exception as e:
            print(f"Error fetching '{query}' from Gnews API: {e}")
    return all_articles 


def fetch_articles_from_api_4(topics, keywords):
    
    all_articles = []

    #News data news
    newsdata_api_key = getattr(settings,'NEWS_DATA_API',None)
    newsdata_url = "https://newsdata.io/api/1/latest"

    for term in topics +keywords:
        params = {
            "apikey": newsdata_api_key,
            "q": term,
            "language": "en"  # adjust as needed
        }
        try:
            response = requests.get(newsdata_url, params=params, timeout=5)
            data = response.json()
            # NewsData.io returns articles under the "results" key
            articles = data.get("results", [])
            for art in articles:
                all_articles.append(art.get("title", "No Title"))
        except Exception as e:
            all_articles.append(f"Error fetching '{term}' from NewsData.io API: {e}")

    return all_articles


# def fetchArticlesFromApi(user, api_key, api_url, apiHead, maxQuery):
#     all_articles = []

#     # existingArticles = Article.objects.filter(user=user, title__in=topics + keywords)
#     # if existingArticles.exists():
#     #     print(list(existingArticles))
#     #     return list(existingArticles)

#     # gnews_api_key = getattr(settings, 'GNEWS_API_KEY', None)
#     # gnews_url = "https://gnews.io/api/v4/top-headlines"

    # for idx in range(maxQuery):
    #     params = {
    #         "token": api_key,
    #         "lang": "en",
    #         "max": 10  # maximum number of articles per request
    #     }
    #     try:
    #         response = requests.get(api_url, params=params, timeout=5)
    #         if response.status_code == 200:
    #             data = response.json()

    #             articles = data.get(apiHead, [])

#     #             for article in articles:
#     #                 new_article, created = Article.objects.get_or_create(
#     #                     user=user,
#     #                     title=article['title'],
#     #                     defaults={
#     #                         'description': article['description'],
#     #                         'url': article.get('url'),
#     #                         'urlToImage': article.get('image'),
#     #                     }
#     #                 )
#     #                 all_articles.append(new_article)
#     #     except Exception as e:
#     #         all_articles.append(f"Error fetching '{term}' from Currents API: {e}")
# 