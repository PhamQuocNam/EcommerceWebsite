from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
GENDER_CHOICE = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100)
    Bio = models.CharField(max_length=100) 
    Birthday = models.DateField(null=True, blank=True)
    Gender = models.CharField(choices=GENDER_CHOICE, max_length=10, default='other')
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username']
    
    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(upload_to="image")
    full_name= models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified= models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name

    

