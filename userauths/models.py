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
    Bio = models.CharField(max_length=100, default="...") 
    Birthday = models.DateField(null=True, blank=True)
    Gender = models.CharField(choices=GENDER_CHOICE, max_length=10, default='other')
    Phone= models.CharField(max_length=15, default="0000000000", null=True)
    Address= models.CharField(max_length=100, null=True)
    City= models.CharField(max_length=100, null=True)
    Country= models.CharField(max_length=100, null=True)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username']
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", default='image/default.jpg')
    full_name = models.CharField(max_length=200, null=True, blank=True, default="ABC")
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.full_name if self.full_name else "Unnamed Profile"


    

