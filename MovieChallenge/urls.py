from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path, include

# カスタム404ビューの指定
handler404 = 'users.views.custom_404_view'  

# ログイン判定して遷移させるビュー (1.ログイン済みならホーム画面、2.未ログインならログイン画面)
def root_router(request):
    if request.user.is_authenticated:
        return redirect('movies:home')  
    else:
        return redirect('users:login') 

# ログイン判定して遷移させるビュー (1.ログイン済みならホーム画面、2.未ログインならログイン画面)
def root_router(request):
    if request.user.is_authenticated:
        return redirect('movies:home')  
    else:
        return redirect('users:login') 
        
urlpatterns = [
    path('', root_router, name='root'),  
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')), 
    path('movies/', include(('movies.urls', 'movies'), namespace='movies')),  
    path('missons/', include(('missions.urls', 'missions'), namespace='missions')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
