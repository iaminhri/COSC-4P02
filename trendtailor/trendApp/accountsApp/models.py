from django.db import models
from django.contrib.auth.models import User
from django.db import migrations

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # image = models.ImageField(upload_to='profile_images/', default='profile_images/')
    role = models.CharField(max_length=255, default='Student')
    phone_number = models.CharField(max_length=15, default='123 456-7890')
    bio = models.TextField(blank=True, default='N/A')
    street_address = models.CharField(max_length=255, default='123 main street')
    city = models.CharField(max_length=100, default='City')
    province = models.CharField(max_length=100, default='Ontario')
    postal_code = models.CharField(max_length=7, default='A1A 1A1')
    birth_date = models.DateField(default='2020-01-01')

    def __str__(self):
        return f"{self.user.username}'s profile"

class ProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_image')
    image = models.ImageField(upload_to='profile_images/', default='profile_images/')