from django.urls import path
from . import views
from .views import SignupView, CustomLogoutView, UserMovieListview
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('home/', UserMovieListview.as_view(),name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
