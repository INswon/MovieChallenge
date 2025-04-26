from django.contrib import admin
from .models import UserMovieRecord, Genre, Review, Mood

# 映画鑑賞記録の管理画面
@admin.register(UserMovieRecord)
class UserMovieRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_watched', 'rating',)  
    search_fields = ('title', 'user__username',)  
    list_filter = ('date_watched', 'rating',)

# 映画ジャンルの管理画面
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 映画レビューの管理画面
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'short_content', 'created_at',)  
    search_fields = ('movie__title', 'user__username', 'content',)  
    list_filter = ('movie', 'user', 'created_at',)  
    ordering = ['-created_at']  # 新しいレビュー順で表示（デフォルトはID順のため変更）

    #レビューの冒頭25文字を表示（長い場合は省略）
    def short_content(self, obj):
        return obj.content[:25] + "..." if len(obj.content) > 25 else obj.content

    short_content.short_description = "レビュー内容"

# ムード(映画鑑賞時感情記録)の管理画面
@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('name',)
