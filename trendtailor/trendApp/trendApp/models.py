from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    urlToImage = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
