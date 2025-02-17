# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sources = models.TextField(help_text="Comma-separated list of news source URLs..")
    topics = models.TextField(help_text="Comma-separated list of topics.")
    keywords = models.TextField(help_text="Comma-separated list of keywords.")

    def get_sources_list(self):
        return [source.strip() for source in self.sources.spilt(',') if source.strip()]

    def get_topics_list(self):
        return [topic.strip() for topic in self.topics.split(',') if topic.strip()]

    def get_keywords_list(self):
        return [keyword.strip() for keyword in self.keywords.split(',') if keyword.strip()]

    def __str__(self):
        return f"Sources: {self.sources}, Topics: {self.topics}, Keywords: {self.keywords}"

class Article(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')  # Optional, for user-specific articles
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    urlToImage = models.URLField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 