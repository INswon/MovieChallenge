from django.urls import path
from .views import MissionListView, UserMissionProgressView, BatchListView

app_name = 'missions'

urlpatterns = [
    path('', MissionListView.as_view(), name='mission_list'),
    path("user_batches/", BatchListView.as_view(), name="user_batch_list"),
    path('progress/', UserMissionProgressView.as_view(), name='user_mission_progress'),
]
