from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from missions.services import MissionCompletionHandler
from .models import Mission, UserMission, Batch, UserBatch
from django.utils.timezone import now

# ミッション一覧を表示するビュー
class MissionListView(LoginRequiredMixin, ListView):

    model = Mission
    template_name = 'missions/mission_list.html'
    context_object_name = 'missions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_missions = UserMission.objects.filter(user=self.request.user)
        user_missions_dict = {um.mission.id: um for um in user_missions}

        mission_status = []
        for mission in self.object_list:
            um = user_missions_dict.get(mission.id)
            mission_status.append({
                'mission': mission,
                'is_completed': um.is_completed if um else False,
                'completed_at': um.completed_at if um else None
            })

        context['mission_status'] = mission_status
        return context

#　ユーザーのミッション進捗状況を表示するビュー
class UserMissionProgressView(LoginRequiredMixin, ListView):

    model = UserMission
    template_name = 'missions/user_mission_progress.html'
    context_object_name = 'user_missions'

    def get_queryset(self):
        return UserMission.objects.filter(user=self.request.user).select_related('mission')

#　バッチ一覧表示リストビュー
class BatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'missions/batch_list.html'
    context_object_name = 'batches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obtained_batches = UserBatch.objects.filter(user=user).values_list('batch', flat=True)
        context['obtained_batches'] = Batch.objects.filter(id__in=obtained_batches)
        context['unobtained_batches'] = Batch.objects.exclude(id__in=obtained_batches)
        return context
    
#　ミッション完了とバッチ付与を管理するクラス
class MissionCompletionHandler:
    @classmethod
    def assign_batch(cls, user):
        mission = Mission.objects.get(title="3本の映画達成")
        watched_movies_count = UserMovieRecord.objects.filter(user=user, is_deleted=False).count()

        if watched_movies_count >= 3:
            user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)
            if not user_mission.is_completed:
                user_mission.is_completed = True
                user_mission.completed_at = now()
                user_mission.save()
                for batch in mission.batches.all():
                    UserBatch.objects.get_or_create(user=user, batch=batch)
        return f"{user.username} にバッチを付与"

    def complete_mission(user, mission):
        user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)
        if user_mission.is_completed:
            return False, "このミッションはすでに完了しています。"
        
        user_mission.is_completed = True
        user_mission.completed_at = now()
        user_mission.save()

        if mission.batches.exists():
            for batch in mission.batches.all():
                UserBatch.objects.get_or_create(user=user, batch=batch)

        return True, f'ミッション「{mission.title}」を完了しました！バッチが付与されました。'
        
#ユーザーがミッションを達成した際に、ミッションを完了し、対応するバッチを付与するビュー
class CompleteMissionView(LoginRequiredMixin, View):
    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)
        success, message = MissionCompletionHandler.complete_mission(request.user, mission)

        if success:
            messages.success(request, message)
        else:
            messages.info(request, message)

        return redirect('missions:mission_list')

