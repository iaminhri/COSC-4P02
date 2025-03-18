from django.db import models
from django.contrib.auth.models import User
from UserPreferenceApp.models import Article 

class ScheduledContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey("UserPreferenceApp.Article", on_delete=models.CASCADE)  
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