from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from missions.services import MissionService
from .models import Mission, UserMission, Batch, UserBatch
from django.utils.timezone import now
from django.http import JsonResponse

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
class BatchListView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        user = request.user
        obtained_batches = UserBatch.objects.filter(user=user).values_list('batch', flat=True)
        obtained_batches_list = Batch.objects.filter(id__in=obtained_batches).values("id", "name", "description")
        unobtained_batches_list = Batch.objects.exclude(id__in=obtained_batches).values("id", "name", "description")

        return JsonResponse({
            "obtained_batches": list(obtained_batches_list),
            "unobtained_batches": list(unobtained_batches_list),
        })
