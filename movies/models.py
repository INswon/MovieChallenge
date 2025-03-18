from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name
    
class UserMovieRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=20)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)  #　映画ポスター画像（任意）
    date_watched = models.DateField()  
    is_deleted = models.BooleanField(default=False)  # 論理削除フラグ（True: 非表示 / データはDBに残る）
    rating = models.IntegerField(default=3)
    genres = models.ManyToManyField(Genre)  #　ユーザーが登録した映画のジャンル（複数可 / 事前登録済みのリストから選択）

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(UserMovieRecord, on_delete=models.CASCADE)
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie}"
