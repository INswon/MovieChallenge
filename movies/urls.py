from django.urls import path
from .views import UserMovieListView, MovieSearchView, MovieRecordDetailView, MovieRecordCreateView, MovieRecordDeleteView, MovieRecordEditView, ReviewPageView
from . import views

app_name = 'movies'

urlpatterns = [
    path('home/', UserMovieListView.as_view(),name='home'),
    path('search/', MovieSearchView.as_view(), name='movie_search'),
    path('movie_create/', views.create_movie_record, name='movie_create'),
    path('detail/<int:pk>/',MovieRecordDetailView.as_view(), name='detail'),
    path('review/', ReviewPageView.as_view(), name='review'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('edit/<int:pk>/', MovieRecordEditView.as_view(), name='edit'),
]
