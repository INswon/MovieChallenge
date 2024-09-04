from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    director = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_on = models.DateField()

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title} on {self.watched_on}"
