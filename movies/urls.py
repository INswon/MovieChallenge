from django.urls import path
from .views import MovieRecordListView, MovieRecordCreateView, MovieRecordDeleteView,MovieRecordEditView

urlpatterns = [
    path('list/',MovieRecordListView.as_view(), name='list'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('edit/<int:pk>/', MovieRecordEditView.as_view(), name='movie_edit'),
]
