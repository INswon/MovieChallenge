from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from movies.models import UserMovieRecord
from .models import ProgressGoal
from missions.models import Batch, UserBatch


def custom_404_view(request, exception):
    return render(request, 'test_templates/404.html', status=404)

# 認証機能 (ログイン機能)
class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # ユーザー作成後にリダイレクト
            return redirect('movies:home')  # 適切なリダイレクト先に変更
        return render(request, 'users/signup.html', {'form': form})    
        
# 認証機能 (ログアウト機能)
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'ログアウトしました')
        return render(request, 'users/logout.html')
    
    
# 進捗目標（モデル作成)
class ProgressGoalCreateView(CreateView):
    model = ProgressGoal
    fields = ['goal_title', 'target_date', 'current_progress']
    template_name = 'users/progressgoal_form.html'
    success_url = reverse_lazy('users:progress_goal_list')  # 成功時のリダイレクト先

    def form_valid(self, form):
        form.instance.user = self.request.user  # ユーザー情報を設定
        return super().form_valid(form)
    
    def get_queryset(self):
        # 現在のユーザーの進捗目標を取得
        return ProgressGoal.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'title' は存在しないため、必要に応じて他のコンテキストを追加
        context['available_badges'] = UserBatch.objects.filter(user=self.request.user).select_related('batch').distinct()
        
        return context
    
# 進捗目標（目標の詳細ページ)
class ProgressGoalDetailView(DetailView):
    model = ProgressGoal
    template_name = 'users/progressgoal_detail.html' 
    context_object_name = 'goals'

# 進捗目標（目標一覧ページ)
class ProgressGoalListView(ListView):
    model = ProgressGoal
    template_name = 'progressgoal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return ProgressGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for goal in context['goals']:
            # missionを通じてbatchを取得
            goal.badges = Batch.objects.filter(mission=goal.mission).distinct() if goal.mission else []
        return context
    
# 進捗目標（目標の削除ページ)
class ProgressGoalDeleteView(DeleteView):
    model = ProgressGoal
    template_name = 'users/progressgoal_confirm_delete.html'
    success_url = reverse_lazy('users:progress_goal_list')

# 進捗目標 (目標の進捗を更新)
class ProgressGoalUpdateView(UpdateView):
    model = ProgressGoal
    fields = ['current_progress']
    template_name = 'progressgoal_update_form.html'
    success_url = reverse_lazy('users:progress_goal_list')  # 成功時のリダイレクト先

# クエスト関連
class QuestCreateView(LoginRequiredMixin, CreateView):
    model = Quest
    form_class = QuestForm
    template_name = 'create_quest.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quest_detail', kwargs={'quest_id': self.object.id})