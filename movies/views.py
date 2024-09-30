from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from movies.models import UserMovieRecord
from django.views.generic import ListView, CreateView 
from django.views.generic.edit import DeleteView 
from .forms import MovieRecordForm
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

class MovieRecordListView(ListView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return UserMovieRecord.objects.filter(user=self.request.user)

class MovieRecordCreateView(CreateView):
    model = UserMovieRecord
    form_class = MovieRecordForm  
    template_name = 'movies/movie_record_create.html'
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
class MovieRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = UserMovieRecord
    template_name = 'movies/movie_record_delete.html'
    success_url = reverse_lazy('users:home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseForbidden()  # 403 Forbidden
        return super().delete(request, *args, **kwargs)

class MovieRecordEditView(UpdateView):
    model = UserMovieRecord
    form_class = MovieRecordForm
    template_name = 'movies/movie_record_edit.html'
    success_url = reverse_lazy('users:home')

