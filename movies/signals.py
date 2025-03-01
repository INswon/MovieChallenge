from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import UserMovieRecord
from missions.services import MissionService

@receiver(post_save, sender=UserMovieRecord)
def auto_assign_batch_on_movie_save(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        print(f"映画記録が追加されました: {instance.title}")

        # 映画視聴数をカウントし、3本達成時にバッチを付与
        MissionService.grant_batch_for_mission(user, "3本の映画達成")
