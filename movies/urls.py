from urllib.parse import quote
from django.urls import path
from .views import UserMovieListView, MovieSearchView, MovieRecordDetailView, MoodArchiveView, RecommendView, ReviewPageView, ThanksPageView, ReviewLikeView, MovieRecordCreateView, MovieRecordDeleteView, MovieRecordEditView
from .views import redirect_to_mood_archive 
from . import views

app_name = 'movies'

urlpatterns = [
    path('home/', UserMovieListView.as_view(),name='home'),
    path('record/',UserMovieListView.as_view() ,name="record"),
    path('detail/<int:pk>/',MovieRecordDetailView.as_view(), name='detail'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
    path('mood_search/', redirect_to_mood_archive, name='mood_search'),
    path('mood_archive/<str:mood_name>/',MoodArchiveView.as_view(), name='mood_archive'),
    path('recommend/<str:recomend_name>/',RecommendView.as_view(), name='recommend'),
    path('movie_create/', views.create_movie_record, name='movie_create'),
    path('review/<int:pk>/', ReviewPageView.as_view(), name='review'),
    path('thanks/', ThanksPageView.as_view(), name='thanks'),
    path('review_like/<int:pk>/', ReviewLikeView.as_view(), name='review_like'),
    path('edit/<int:pk>/', MovieRecordEditView.as_view(), name='edit'),
]
