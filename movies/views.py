from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from movies.models import UserMovieRecord
from missions.models import Batch, UserBatch
from .forms import MovieRecordForm, MovieSearchForm
from django.views import View
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from missions.models import Mission
from .services import TmdbMovieService
from datetime import date


def create_movie_record(request):
    if request.method == "POST":
        UserMovieRecord.objects.create(
            title=request.POST["title"],
            poster=request.POST["poster"],
            rating=int(request.POST["rating"]),
            comment=request.POST["comment"],
            date_watched=date.today(),
            user=request.user  
        )
        return redirect("movies:home")  

    else:
        return render(request, "movies/movie_create.html", {
        "title": request.GET.get("title"),
        "poster": request.GET.get("poster"),
        "director": request.GET.get("director"),
        "genres": request.GET.get("genres"),
    })


# 映画鑑賞記録一覧表示機能
class UserMovieListView(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'movies/home.html'
    context_object_name = 'records'

    def get_queryset(self):
        return UserMovieRecord.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = MovieSearchForm(self.request.GET or None)
        context["form"] = form  # 検索フォームをテンプレートに渡す
        
        if form.is_valid():
            query = form.cleaned_data["movie_title"]
            print(f"検索クエリ: {query}")  # デバッグログ
            context["movies"] = TmdbMovieService.search(query) if query else []
            print(f"検索結果: {context['movies']}")  # デバッグログ
        else:
            print(f"フォームエラー: {form.errors}")  # フォームエラーログ
        
        return context

# 映画鑑賞記録詳細表示機能
class MovieRecordDetailView(LoginRequiredMixin, DetailView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_detail.html'  
    context_object_name = 'record'


# 映画情報の取得検索
class MovieSearchView(TemplateView):
    template_name = "movies/movie_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        print(f"検索クエリ: {query}")  # ✅ デバッグ用
        context["movies"] = TmdbMovieService.search(query) if query else []
        print(f"検索結果: {context['movies']}")  # ✅ デバッグ用
        return context


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

