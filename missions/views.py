from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from .models import Mission, UserMission, Batch, UserBatch

#ユーザーが利用可能なすべてのミッションを一覧表示するビュー
class MissionListView(LoginRequiredMixin, ListView):

    model = Mission
    template_name = 'mission/mission_list.html'
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

#ユーザーのミッション進捗状況を表示するビュー
class UserMissionProgressView(LoginRequiredMixin, ListView):

    model = UserMission
    template_name = 'mission/user_mission_progress.html'
    context_object_name = 'user_missions'

    def get_queryset(self):
        return UserMission.objects.filter(user=self.request.user).select_related('mission')


#ユーザーが取得したバッチを一覧表示するビュー
class UserBatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'missions/batch_list.html'
    context_object_name = 'batches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        obtained_batch_ids = UserBatch.objects.filter(user=user).values_list('batch', flat=True)
        context['obtained_batches'] = Batch.objects.filter(id__in=obtained_batch_ids)
        context['unobtained_batches'] = Batch.objects.exclude(id__in=obtained_batch_ids)

        return context


#ユーザーがミッションを達成した際に、ミッションを完了し、対応するバッチを付与するビュー
class CompleteMissionView(LoginRequiredMixin, View):
    
    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)
        user_mission, created = UserMission.objects.get_or_create(user=request.user, mission=mission)

        if user_mission.is_completed:
            messages.info(request, 'このミッションはすでに完了しています。')
        else:
            # ミッションの達成条件を確認
            user_mission.is_completed = True
            user_mission.completed_at = timezone.now()
            user_mission.save()

            # バッチを付与
            for batch in mission.batches.all():
                UserBatch.objects.get_or_create(user=request.user, batch=batch)

            messages.success(request, f'ミッション「{mission.title}」を完了しました！バッチが付与されました。')

        return redirect('mission:mission_list')
