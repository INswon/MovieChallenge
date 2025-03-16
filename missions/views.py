from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from missions.services import MissionService
from .models import Mission, UserMission, Batch, UserBatch
from django.utils.timezone import now
from django.http import JsonResponse
import json

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

# バッチ一覧表示リストビュー
class BatchListTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "missions/batch_list.html")
    
# バッチ一覧表示リストビュー
class BatchListView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        obtained_batches = UserBatch.objects.filter(user=user)
        
        obtained_list = []
        for user_batch in obtained_batches:
            batch = user_batch.batch
            obtained_list.append({
                "id": batch.id,
                "name": batch.name,
                "description": batch.description,
                "icon": batch.icon.url if batch.icon else ""  
            })

        all_batch_ids = Batch.objects.values_list('id', flat=True)
        user_batch_ids = obtained_batches.values_list('batch_id', flat=True)
        unobtained_list = []
        for b in Batch.objects.filter(id__in=all_batch_ids.difference(user_batch_ids)):
            unobtained_list.append({
                "id": b.id,
                "name": b.name,
                "description": b.description,
                "icon": b.icon.url if b.icon else ""
            })

        response_data = {
            "obtained_batches": obtained_list,
            "unobtained_batches": unobtained_list,
        }
        return JsonResponse(response_data)
