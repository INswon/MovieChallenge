from django.urls import path
from .views import SignupView, CustomLogoutView, ProgressGoalCreateView, ProgressGoalUpdateView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('goals/create/',ProgressGoalCreateView.as_view(), name='progress_goal_create'),
    path('goals/update/<int:pk>/', ProgressGoalUpdateView.as_view(), name='progress_goal_update'),
]
