from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.conf import settings

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sources = models.TextField(help_text="Comma-separated list of news source URLs..")
    topics = models.TextField(help_text="Comma-separated list of topics.")
    keywords = models.TextField(help_text="Comma-separated list of keywords.")

    def get_sources_list(self):
        return [source.strip() for source in self.sources.split(',') if source.strip()]

    def get_topics_list(self):
        return [topic.strip() for topic in self.topics.split(',') if topic.strip()]

    def get_keywords_list(self):
        return [keyword.strip() for keyword in self.keywords.split(',') if keyword.strip()]

    def __str__(self):
        return f"Sources: {self.sources}, Topics: {self.topics}, Keywords: {self.keywords}"

class Article(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')  # Optional, for user-specific articles
    title = models.CharField(max_length=500, default='Untitled news article', null=True)
    description = models.TextField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    urlToImage = models.URLField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    topic = models.CharField(max_length=200, default='news')
    keyword = models.JSONField(default=list, blank=True, null=True)

    # Many-to-Many Relationship
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='LikedBy',
        related_name='liked_articles'
    )
    
    def __str__(self):
        return self.title

class ArticleFrench(models.Model):
    original = models.OneToOneField('Article', on_delete=models.CASCADE, related_name='french')
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    urlToImage = models.URLField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=200)

    # Many-to-Many Relationship
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='LikedBy',
        related_name='liked_articles_french'
    )

    def __str__(self):
        return self.title
    
class LikedBy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes_user'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, blank=True, 
        null=True, related_name='likes_article'
    )
    article_french = models.ForeignKey(
        ArticleFrench, on_delete=models.CASCADE, 
        blank=True, null=True,
        related_name='likes_article_french'
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.article:
            return f"{self.user.username} liked {self.article.title} (EN)"
        elif self.article_french:
            return f"{self.user.username} liked {self.article_french.title} (FR)"
        else:
            return f"{self.user.username} liked unknown article"

class ScheduledContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)  
    schedule_date = models.DateTimeField()
    repeat_option = models.CharField(
        max_length=20,
        choices=[
            ("none", "No Repeat"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
        ],
        default="none",
    )

    def __str__(self):
        return f"{self.user.username} - {self.article.title} - {self.schedule_date}"    