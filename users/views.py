from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
from movies.models import UserMovieRecord
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class UserMovieListview(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'users/home.html'
    context_object_name = 'records'
    login_url = '/login/'  

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

class ProgressGoalCreateView(CreateView):
    model = ProgressGoal
    fields = ['goal_title', 'target_date', 'current_progress']
    template_name = 'users/progressgoal_form.html'
    success_url = reverse_lazy('progress_goal_list')  # 成功時のリダイレクト先

    def form_valid(self, form):
        form.instance.user = self.request.user  # 現在のユーザーを設定
        return super().form_valid(form)
    
class ProgressGoalUpdateView(UpdateView):
    model = ProgressGoal
    fields = ['progress']
    template_name = 'progressgoal_update_form.html'
    success_url = reverse_lazy('progress_goal_list')  # 成功時のリダイレクト先
    

