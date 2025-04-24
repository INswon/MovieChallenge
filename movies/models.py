from django.db import models
from django.contrib.auth.models import User

# 映画ジャンル（ユーザーの映画記録とManyToManyで紐づく）
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name
        
# ユーザーごとの映画鑑賞記録
class UserMovieRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=20)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)  #　映画ポスター画像（任意）
    poster_url = models.URLField(blank=True, null=True)  # APIから取得した画像URL用
    date_watched = models.DateField()  
    is_deleted = models.BooleanField(default=False)  # 論理削除フラグ（True: 非表示 / データはDBに残る）
    director = models.CharField(max_length=255, blank=True)
    comment =  models.TextField(blank=True)  # 感想（任意）
    rating = models.IntegerField(default=3)
    genres = models.ManyToManyField(Genre)  
    tmdb_id = models.IntegerField(blank=True, null=True) #特定の映画情報を TMDb API から再取得するためのID

    def __str__(self):
        return f"{self.title} - {self.user.username}"

# 映画に対するレビュー（感想投稿）
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(UserMovieRecord, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=3)
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
        
    # レビューに紐づくいいね数を取得（逆参照でカウント）
    def like_count(self):
        return self.like_set.count()

    def __str__(self):
        content_preview = self.content[:20] + ('...' if len(self.content) > 20 else '')
        return f"{self.user.username} {content_preview} - {self.created_at.strftime('%Y-%m-%d')} ({self.movie.user} - {self.movie.title})"

# いいね記録（1ユーザー1回制限）
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    # 同一ユーザーが同じレビューに複数回いいねできないよう制約を設定
    class Meta:
        constraints =[
            models.UniqueConstraint(fields=["user", "review"], name="unique_user_review_like"),
        ]

# ユーザーの感情をタグとして管理(#興奮, #新鮮, #癒された,#前向きになれた)
class Mood(models.Model):
    name = models.CharField(max_length=10)

