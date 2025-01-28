from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any additional fields you want here
    pass
class Movie(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE, related_name ="Movie")
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
    def __str__(self):
        return self.title
    def serialize(self):
        return {
            "id": self.id,
            "userid": self.userid.id,  # Return user ID instead of full user object
            "title": self.title,
            "released": self.released,
            "rated": self.rated,
            "runtime": self.runtime,
            "genre": self.genre,
            "director": self.director,
            "actors": self.actors,
            "trailer": self.trailer,
            "plot": self.plot,
            "poster": self.poster
        }
