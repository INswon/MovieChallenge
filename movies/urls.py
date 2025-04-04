from django.urls import path
from .views import UserMovieListView, MovieRecordDetailView, MovieRecordCreateView, MovieRecordDeleteView, MovieRecordEditView
from .services import MovieSerchView

app_name = 'movies'

urlpatterns = [
    path('home/', UserMovieListView.as_view(),name='home'),
    path('search/', MovieSerchView.as_view(), name='search_movies'),
    path('detail/<int:pk>/',MovieRecordDetailView.as_view(), name='detail'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('edit/<int:pk>/', MovieRecordEditView.as_view(), name='edit'),
]
