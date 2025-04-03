from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProgressGoal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_title = models.CharField(max_length=200)  # 目標タイトル
    target_date = models.DateField()  # 目標達成日
    current_progress = models.IntegerField(default=0)  # 現在の進捗状況
    total_movies = models.IntegerField()  # 目標の映画鑑賞数
    genre_preferences = models.CharField(max_length=200, blank=True)  # ジャンルの好み
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')  # 目標の状態
    movies_watched = models.TextField(blank=True)  # 鑑賞した映画のリスト
    movie_ratings = models.TextField(blank=True)  # 映画の評価や感想

    def __str__(self):
        return f"{self.goal_title} - {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(UserMovieRecord, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies' 
    )

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"{self.user} - {self.movie} - {'Reply' if self.is_reply() else 'Review'}"



