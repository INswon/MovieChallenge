from django.urls import path
from .views import SignupView, CustomLogoutView, MovieRecordListView, MovieRecordCreateView, MovieRecordDeleteView
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('home/',views.home, name="home"),
    path('list/',MovieRecordListView.as_view(), name='list'),
    path('create/',MovieRecordCreateView.as_view(), name="create"),
    path('delete/<int:pk>/',MovieRecordDeleteView.as_view(), name="delete"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
