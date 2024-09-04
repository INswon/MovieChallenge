from django.urls import path
from .views import SignupView 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('home/',views.home, name="home"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
