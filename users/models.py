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

# アプリ作成者が設定するミッションとバッジ

class Mission(models.Model):
    title = models.CharField(max_length=200)  # ミッションタイトル
    description = models.TextField(blank=True)  # ミッションの詳細説明
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時

    def __str__(self):
        return self.title

class Badge(models.Model):
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='badge')  # Missionとの1対1の関係
    name = models.CharField(max_length=100)  # バッジ名
    description = models.TextField()  # バッジの説明
    icon = models.ImageField(upload_to='badges/')  # アイコン画像

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'badge')  # ユーザーとバッジの組み合わせを一意にする

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

# ユーザーごとのミッション完了状況を追跡するモデルの追加

class UserMission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_missions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='user_missions')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'mission')  # ユーザーとミッションの組み合わせを一意にする

    def __str__(self):
        status = "Completed" if self.is_completed else "Incomplete"
        return f"{self.user.username} - {self.mission.title} ({status})"
