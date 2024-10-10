from django.db import models
from django.contrib.auth.models import User

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
    status = models.CharField(max_length=20, choices=  STATUS_CHOICES, default='active')  # 目標の状態
    movies_watched = models.TextField(blank=True)  # 鑑賞した映画のリスト
    movie_ratings = models.TextField(blank=True)  # 映画の評価や感想

    def __str__(self):
        return f"{self.goal_title} - {self.user.username}"

class Quest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quests')
    title = models.CharField(max_length=200)  # クエストタイトル
    description = models.TextField(blank=True)  # クエストの詳細説明
    reward = models.CharField(max_length=200, blank=True)  # クエスト達成時の報酬（バッジ名など）
    is_completed = models.BooleanField(default=False)  # クエストの達成状況
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    completed_at = models.DateTimeField(null=True, blank=True)  # 完了日時

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    

class Mission(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='missions')
    title = models.CharField(max_length=200)  # ミッションタイトル
    description = models.TextField(blank=True)  # ミッションの詳細説明
    is_completed = models.BooleanField(default=False)  # ミッションの達成状況
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    completed_at = models.DateTimeField(null=True, blank=True)  # 完了日時

    def __str__(self):
        return f"{self.title} - {self.quest.title}"

class Badge(models.Model):
    name = models.CharField(max_length=100)  # バッジ名
    description = models.TextField()          # バッジの説明
    icon = models.ImageField(upload_to='badges/')  # アイコン画像

    def __str__(self):
        return self.name
