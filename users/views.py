from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import QuestForm
from movies.models import UserMovieRecord 
from .models import ProgressGoal, Quest, Mission


def custom_404_view(request, exception):
    return render(request, 'test_templates/404.html', status=404)

class UserMovieListview(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'users/home.html'
    context_object_name = 'records'
    login_url = '/users/login/'  

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # ユーザー作成後にリダイレクト
            return redirect('users:home')  # 適切なリダイレクト先に変更
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

    def get_queryset(self):
        # 現在のユーザーの進捗目標を取得
        return ProgressGoal.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for goal in context['goals']:
            # 各進捗目標に関連するバッジやミッションを取得
            goal.badges = Badge.objects.filter(mission__quest__progressgoal=goal).distinct()
        return context
    
class ProgressGoalListView(ListView):
    model = ProgressGoal
    template_name = 'progressgoal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        # 現在のユーザーの進捗目標を取得
        return ProgressGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for goal in context['goals']:
            # 各進捗目標に関連するバッジやミッションを取得
            goal.badges = Badge.objects.filter(mission__quest__progressgoal=goal).distinct()
        return context
    

class ProgressGoalUpdateView(UpdateView):
    model = ProgressGoal
    fields = ['progress']
    template_name = 'progressgoal_update_form.html'
    success_url = reverse_lazy('progress_goal_list')  # 成功時のリダイレクト先


class QuestCreateView(LoginRequiredMixin, CreateView):
    model = Quest
    form_class = QuestForm
    template_name = 'create_quest.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quest_detail', kwargs={'quest_id': self.object.id})

    
