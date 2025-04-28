from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class ArchivedContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    platform = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)
    original_article_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True, max_length=200)
    created_date = models.DateTimeField('Date Created', default=timezone.now)

    def __str__(self):
        return self.email