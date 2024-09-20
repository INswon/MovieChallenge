from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.views import View
from movies.models import UserMovieRecord
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    records = UserMovieRecord.objects.filter(user=request.user)
    return render(request, 'users/home.html', {'records': records}) 

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # 会員登録後のリダイレクト先を指定
        return render(request, 'users/signup.html', {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'ログアウトしました')
        return render(request, 'users/logout.html')
