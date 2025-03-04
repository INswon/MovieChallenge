import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import UserMovieRecord
from missions.services import MissionService
from django.utils.timezone import localtime

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserMovieRecord)
def auto_assign_batch_on_movie_save(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        logger.debug(f"シグナル実行: {instance.title} (User: {user.username})")

        #「3本の映画視聴達成」のミッション
        MissionService.grant_batch_for_mission(user, "3本の映画達成")
        logger.debug(f"MissionService.grant_batch_for_mission() 実行完了: {user.username}")

        #「1日3本の映画視聴達成」のミッション
        today = instance.date_watched  
        today_movie_count = UserMovieRecord.objects.filter(user=user, date_watched=today).count()

        if today_movie_count >= 3:
            MissionService.grant_batch_for_mission(user, "1日3本の映画視聴達成")
            logger.debug(f"1日3本の映画視聴達成バッチを付与: {user.username} ({today_movie_count}本)")
