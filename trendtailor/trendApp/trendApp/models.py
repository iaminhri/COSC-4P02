from django.db import models

class Preferences(models.Model):
    sources = models.TextField()   
    topics = models.TextField()   
    keywords = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Sources: {self.sources}, Topics: {self.topics}, Keywords: {self.keywords}"
