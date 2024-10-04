from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

handler404 = 'users.views.custom_404_view'  # カスタム404ビューの指定

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')), 
    path('movie/', include(('movies.urls'), namespace='movies')),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

