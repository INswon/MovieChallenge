from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from movies.models import UserMovieRecord
from missions.models import Batch, UserBatch
from .forms import MovieRecordForm
from django.views import View
from django.shortcuts import render
from missions.models import Mission
from missions.utils import MissionCompletionHandler

#映画鑑賞記録一覧表示機能
class UserMovieListView(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'movies/home.html'
    context_object_name = 'records'

#映画鑑賞記録詳細表示機能
class MovieRecordDetailView(DetailView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_detail.html'  
    context_object_name = 'record'

#映画鑑賞記録新規作成機能
class MovieRecordCreateView(CreateView):
    model = UserMovieRecord
    form_class = MovieRecordForm
    template_name = 'movies/movie_record_create.html'
    success_url = reverse_lazy('movies:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        try:
            print("バッジ処理開始")
            MissionCompletionHandler.assign_batch(self.request.user)
            print("バッジ処理完了")
        except Exception as e:
            print("バッジ処理エラー:", e)

        return response


# 映画鑑賞記録削除機能
class MovieRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_delete.html'
    success_url = reverse_lazy('movies:home') 

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseForbidden()  
        
        self.object.is_deleted = True
        self.object.save()
        
        self.remove_batch_if_ineligible(request.user)
        
        return super().delete(request, *args, **kwargs)

    @classmethod
    def remove_batch_if_ineligible(cls, user):
        #鑑賞数が条件を満たさなくなった場合、バッジを取り消す

        watched_count = UserMovieRecord.objects.filter(user=user, is_deleted=False).count()
        if watched_count < 3:  
            UserBatch.objects.filter(user=user, batch__name="鑑賞3作品達成バッジ").delete()
            print("バッジが削除されました：鑑賞3作品達成バッジ")


#映画鑑賞編集機能
class MovieRecordEditView(LoginRequiredMixin, UpdateView):
    model = UserMovieRecord
    form_class = MovieRecordForm
    template_name = 'movies/movie_record_edit.html'
    success_url = reverse_lazy('movies:home')

    def save(self, commit=True):
          instance = super().save(commit=False)
          
          if self.cleaned_data.get("delete_poster"):
            if instance.poster:
                instance.poster.delete(save=False)
            instance.poster = None

          if commit:
              instance.save()
          return instance
