from django.contrib import admin
from .models import  UserMovieRecord

# WatchHistory モデルを管理画面に登録
admin.site.register(UserMovieRecord)