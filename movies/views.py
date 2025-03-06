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

# 映画鑑賞記録一覧表示機能
class UserMovieListView(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'movies/home.html'
    context_object_name = 'records'

    def get_queryset(self):
        return UserMovieRecord.objects.filter(user=self.request.user)

# 映画鑑賞記録詳細表示機能
class MovieRecordDetailView(LoginRequiredMixin, DetailView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_detail.html'  
    context_object_name = 'record'

# 映画鑑賞記録新規作成機能
class MovieRecordCreateView(LoginRequiredMixin, CreateView):
    model = UserMovieRecord
    form_class = MovieRecordForm
    template_name = 'movies/movie_record_create.html'
    success_url = reverse_lazy('movies:home')

    def form_valid(self, form):
        form.instance.user = self.request.user

        if not form.cleaned_data.get("poster"):
            form.instance.poster = None

        return super().form_valid(form)

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
        
        return super().delete(request, *args, **kwargs)

# 映画鑑賞編集機能
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
