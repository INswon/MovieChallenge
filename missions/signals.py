import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import UserMovieRecord
from missions.services import MissionService

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserMovieRecord)
def auto_assign_batch_on_movie_save(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        logger.debug(f"シグナル実行: {instance.title} (User: {user.username})")

        MissionService.grant_batch_for_mission(user, "3本の映画達成")

        logger.debug(f"MissionService.grant_batch_for_mission() 実行完了: {user.username}")
