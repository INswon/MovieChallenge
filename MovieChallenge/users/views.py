from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View

def home(request):
    return render(request, 'users/home.html')

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
