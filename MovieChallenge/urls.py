from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from movies.views import YourView  

handler404 = 'users.views.custom_404_view'  # カスタム404ビューの指定

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')), 
    path('movie/', include(('movies.urls', 'movies'), namespace='movies')),  
    path('missons/', include(('missions.urls', 'missions'), namespace='missions')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
