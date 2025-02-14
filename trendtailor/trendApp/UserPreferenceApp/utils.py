import requests
from django.conf import settings

def fetch_articles_from_api(topics, keywords):
    """Fetch articles using an external News API, filtered by topics/keywords."""
    # Hard-coded API key
    api_key = getattr(settings,'NEWS_API_KEY',None)

    if not api_key:
        raise ValueError("API Key is not found")

    all_articles = []
    for topic in topics + keywords:
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            articles = data.get('articles', [])
            for art in articles:
                all_articles.append(art['title'])
        except Exception as e:
            all_articles.append(f"Error fetching topic {topic}: {e}")

    #Gnews
    gnews_api_key = getattr(settings,'GNEWS_API_KEY',None)
    gnews_url = "https://gnews.io/api/v4/top-headlines"


    # Here we loop over each topic. You could also loop over keywords if desired.
    for term in topics + keywords:
        params = {
            "token": gnews_api_key,
            "q": term,
            "lang": "en",
            "max": 10  # maximum number of articles per request
        }
        try:
            response = requests.get(gnews_url, params=params, timeout=5)
            data = response.json()
            articles = data.get('articles', [])
            for art in articles:
                all_articles.append(art.get('title', 'No Title'))
        except Exception as e:
            all_articles.append(f"Error fetching '{term}' from GNews: {e}")

    #current news
    currents_api_key = getattr(settings, 'CURRENT_API_KEY',None)
    currents_url = "https://api.currentsapi.services/v1/search"

    #all_articles = []
    for term in topics + keywords:
        params = {
            "apiKey": currents_api_key,
            "q": term,
            "language": "en"
        }
        try:
            response = requests.get(currents_url, params=params, timeout=5)
            data = response.json()
            # The Currents API returns articles under the "news" key.
            articles = data.get("news", [])
            for art in articles:
                all_articles.append(art.get('title', 'No Title'))
        except Exception as e:
            all_articles.append(f"Error fetching '{term}' from Currents API: {e}")

    return all_articles
