from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import WatchHistory

class TimelineView(LoginRequiredMixin, ListView):
    model = WatchHistory
    template_name = 'timeline.html'
    context_object_name = 'watch_history'
    ordering = ['-watched_on']
    
    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)
    

    
