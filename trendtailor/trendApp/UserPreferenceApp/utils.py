import requests

def fetch_articles_from_api(topics, keywords):
    """Fetch articles using an external News API, filtered by topics/keywords."""
    # Hard-coded API key
    api_key = "7a0f6618f66a42499590fae55805b817"

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
    return all_articles

