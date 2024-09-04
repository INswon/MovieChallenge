from django.urls import path
from . import views

urlpatterns = [
    path('',views.TimelineView.as_view(), name='timeline_view'),
]
