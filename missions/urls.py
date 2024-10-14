from django.urls import path
from .views import MissionListView, UserMissionProgressView, UserBatchListView, CompleteMissionView

app_name = 'mission'

urlpatterns = [
    path('', MissionListView.as_view(), name='mission_list'),
    path('progress/', UserMissionProgressView.as_view(), name='user_mission_progress'),
    path('batches/', UserBatchListView.as_view(), name='user_batches'),
    path('complete/<int:mission_id>/', CompleteMissionView.as_view(), name='complete_mission'),
]
