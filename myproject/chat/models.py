from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any additional fields you want here
    pass
class Movie(models.Model):
    title = models.CharField(max_length=100)
    released =models.CharField(max_length=200)
    rated = models.CharField(max_length=40)
    runtime =models.CharField(max_length=40)
    Genre = models.CharField(max_length=50)
    Director = models.CharField(max_length=60)
    Actors = models.CharField(max_length=100)
    trailer = models.CharField(max_length=50)
    plot = models.CharField(max_length=300)
    poster =models.CharField(max_length=200)

