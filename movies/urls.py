from urllib.parse import quote
from django.urls import path
from .views import UserMovieListView, RecordView, MovieRecordDetailView, MovieRecordCreateView, MovieRecordDeleteView, MovieRecordEditView, MovieSearchView, MoodArchiveView, RecommendSelectView, RecommendListView, ReviewPageView, ThanksPageView, ReviewLikeView
from .views import redirect_to_mood_archive 
from . import views

app_name = 'movies'

urlpatterns = [
    # 1. ホーム
    path('home/', UserMovieListView.as_view(),name='home'),

    # 2. 映画記録
    path('record/',RecordView.as_view() ,name="record"),
    path('detail/<int:pk>/',MovieRecordDetailView.as_view(), name='detail'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('movie_create/', views.create_movie_record, name='movie_create'),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('edit/<int:pk>/', MovieRecordEditView.as_view(), name='edit'),

    # 3. 検索(映画作品検索, 感情検索)
    path('search/', MovieSearchView.as_view(), name='movie_search'),
    path('mood_search/', redirect_to_mood_archive, name='mood_search'),

    # 4. 感情アーカイブ
    path('mood_archive/<str:mood_name>/',MoodArchiveView.as_view(), name='mood_archive'),

    # 5. 映画推薦
    path('recommend/',RecommendSelectView.as_view(), name='recommend_select'),
    path('recommend/<str:recommend_name>/',RecommendListView.as_view(), name='recommend'),
    
    # 6. レビュー
    path('review/<int:pk>/', ReviewPageView.as_view(), name='review'),
    path('thanks/', ThanksPageView.as_view(), name='thanks'),
    path('review_like/<int:pk>/', ReviewLikeView.as_view(), name='review_like'),
]
