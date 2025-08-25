from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.db.models import Count
from movies.models import UserMovieRecord, Genre, Mood, Review, Like
from movies.constants import MOOD_CATEGORY_MAP, MOOD_HERO_IMAGES
from .forms import MovieRecordForm, MovieSearchForm, UserReviewForm
from django.views import View
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView
from .services import TmdbMovieService
from datetime import date
import re

def parse_mood_names(text: str):
    s = (text or "").replace("　"," ").strip()
    tokens = re.split(r"[、,\s]+", s)
    names = [t.strip().lstrip("#") for t in tokens if t and t.strip()]
    return list(dict.fromkeys(names))

def get_or_create_mood_objects(mood_text):
    names = parse_mood_names(mood_text)
    return [Mood.objects.get_or_create(name=n)[0] for n in names]

#特定の感情アーカイブページへのアクセス設定 (該当するページがなければホームページにリダイレクト)
def redirect_to_mood_archive(request):
    mood = request.GET.get("mood", "").strip().lstrip("#")
    if mood:
        return redirect("movies:mood_archive", mood_name=mood)  
    return redirect("movies:home")

# タイトル、ポスターURL、監督、ジャンルをAPIから取得し、UserMovieRecordに保存
def create_movie_record(request):
    if request.method == "POST":
        mood_text = request.POST.get("mood", "")
        mood_objs = get_or_create_mood_objects(mood_text)

        record = UserMovieRecord.objects.create(
            title=request.POST["title"],
            poster_url=request.POST["poster"], 
            director=request.POST["director"],  
            rating=int(request.POST["rating"]),
            comment=request.POST["comment"],
            date_watched=date.today(),
            user=request.user 
        )

        genre_names = request.POST["genres"].split(", ")
        genre_objs = []
        for name in genre_names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_objs.append(genre)
        record.genres.set(genre_objs)

        record.mood.set(mood_objs)

        return redirect("movies:home")

    else:
        movie_id = request.GET.get("movie_id")
        context = {}

        if movie_id:
            movie_info = TmdbMovieService.get_movie_info(movie_id)
            if movie_info:
                context = {
                    "title": movie_info["title"],
                    "poster": movie_info["poster_url"],
                    "director": movie_info["director"],
                    "genres": ", ".join(movie_info["genres"]),
                    "rating_choices": range(1, 6)
                }

        return render(request, "movies/movie_create.html", context)

# 映画鑑賞記録一覧表示機能
class UserMovieListView(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = 'movies/home.html'
    context_object_name = 'records'

    #感情タグの検索フィルタリング
    def get_queryset(self):
        qs = UserMovieRecord.objects.filter(user=self.request.user)
        moods = self.request.GET.get("mood", "")
        tags = parse_mood_names(moods)
        if tags:
            qs = qs.filter(mood__name__in=tags).distinct()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        top_moods = (
            Mood.objects
            .filter(usermovierecord__user=user)
            .annotate(num_records=Count("usermovierecord"))
            .order_by("-num_records", "id")[:4]  
        )
        context["top_moods"] = top_moods
        context["category_classes"] = {
            m.name: MOOD_CATEGORY_MAP.get(m.name, "default") for m in top_moods
        }

        form = MovieSearchForm(self.request.GET or None)
        context["form"] = form  
     
        if form.is_valid():
            query = form.cleaned_data["movie_title"]
            context["movies"] = TmdbMovieService.search(query) if query else []        
        return context
    
# 感情アーカイブページ一覧
class MoodArchiveView(LoginRequiredMixin, ListView):
    model = UserMovieRecord
    template_name = "movies/mood_archive.html"
    context_object_name = "mood_archive"

    def get_queryset(self):
        mood_name = self.kwargs["mood_name"]
        return (
            UserMovieRecord.objects
            .filter(user=self.request.user, mood__name=mood_name)
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mood_name = self.kwargs.get("mood_name")
        mood_obj  = Mood.objects.filter(name=mood_name).first()
        user = self.request.user

        filter_moods = Mood.objects.filter(usermovierecord__user=user).distinct()
        user_moods = (
            filter_moods
            .annotate(num_records=Count("usermovierecord"))
            .order_by("-num_records", "id")[:4]
        )

        has_records = context["mood_archive"].exists()

        hero_image = None
        category = None
        if has_records:
            category = MOOD_CATEGORY_MAP.get(mood_name, "default")
            hero_image = MOOD_HERO_IMAGES.get(category, "images/hero/default.jpg")

        category_classes = {
            m.name: MOOD_CATEGORY_MAP.get(m.name, "default")
            for m in user_moods
        }

        context["mood_name"] = mood_name
        context["mood"] = mood_obj
        context["top_moods"] = user_moods
        context["category_class"] = category
        context["hero_image"] = hero_image
        context["category_classes"] = category_classes
        context["has_records"] = has_records
        
        return context

# 映画鑑賞記録詳細表示機能
class MovieRecordDetailView(LoginRequiredMixin, DetailView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_detail.html'  
    context_object_name = 'record'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record = self.object

        #(後コメント考案) TMDb API から映画情報を取得（なければローカルの情報を使用）
        api_data = TmdbMovieService.get_movie_info(record.tmdb_id) if record.tmdb_id else None

        movie_data ={
            "title": api_data.get("title") if api_data else record.title,
            "poster_url": api_data.get("poster_url") if api_data else record.poster_url,
            "director": api_data.get("director") if api_data else record.director,
            "genres": api_data.get("genres") if api_data else record.genres.all(),
        }

        context["movie_data"] = movie_data

       # 他のユーザーのレビュー 一覧（作成日時順）
        other_reviews = Review.objects.filter(movie=record).exclude(user=self.request.user).order_by("created_at")

        #「ログイン中ユーザーがいいね済みかどうか」のフラグを付与 (テンプレート側で「❤️ / 🤍」の表示切り替えに使用)
        for review in other_reviews:
            review.is_liked_by_user = review.like_set.filter(user=self.request.user).exists()

        context["other_reviews"] = other_reviews

        return context

# ユーザーによる映画レビューの投稿ビュー
class ReviewPageView(LoginRequiredMixin,CreateView):
    model = Review
    form_class = UserReviewForm
    template_name = "movies/movie_review.html"
    success_url = reverse_lazy("movies:thanks")

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(UserMovieRecord, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie = self.movie
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.movie 
        return context

# レビュー投稿確認ページ遷移
class ThanksPageView(TemplateView):
    template_name = "movies/movie_thanks.html"

# AjaxのLoginRequiredMixinの定義
class AjaxLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "ログインが必要です"}, status=403)
            return self.handle_no_permission()  # 通常の302リダイレクト
        return super().dispatch(request, *args, **kwargs)

# レビューのいいね機能処理
class ReviewLikeView(AjaxLoginRequiredMixin,View):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        user = request.user

        like = Like.objects.filter(user=user, review=review).first()
        liked = False

        if like:
            like.delete()
        else:
            Like.objects.create(user=user, review=review, movie=review.movie)
            liked = True

        count = review.like_set.count()
        return JsonResponse({"liked": liked, "count": count})
    
# 映画情報の取得検索
class MovieSearchView(LoginRequiredMixin, TemplateView):
    template_name = "movies/movie_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context["movies"] = TmdbMovieService.search(query) if query else []
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
        return redirect(self.success_url)

# 映画鑑賞編集機能
class MovieRecordEditView(LoginRequiredMixin, UpdateView):
    model = UserMovieRecord
    form_class = MovieRecordForm
    template_name = 'movies/movie_record_edit.html'
    success_url = reverse_lazy('movies:home')

    def get_queryset(self):
        return UserMovieRecord.objects.filter(user=self.request.user)