from django.db import models
from django.contrib.auth.models import User

class UserMovieRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # 映画タイトル
    poster = models.ImageField(upload_to='posters/')  # 映画ポスター画像
    date_watched = models.DateField()  # 鑑賞日
    rating = models.IntegerField()  # 映画評価 (例: 1から5の評価)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
