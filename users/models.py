from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    
    # To make migrations to auth_user table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional row to add in auth_user table
    image = models.ImageField(default='profile.jpg', upload_to='profile_pictures')
    contact_number = models.CharField(max_length=255,default="999999999")