from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import UserMovieRecord
from missions.services import MissionService
from django.utils.timezone import localtime

@receiver(post_save, sender=UserMovieRecord)
def auto_assign_batch_on_movie_save(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user

    #「3本の映画視聴達成」のミッション
    MissionService.grant_batch_for_mission(user, "3本の映画達成")

    #「1日3本の映画視聴達成」のミッション
    today = instance.date_watched  
    today_movie_count = UserMovieRecord.objects.filter(user=user, date_watched=today).count()

    if today_movie_count >= 3:
        MissionService.grant_batch_for_mission(user, "1日3本の映画視聴達成")
        print(f"1日3本の映画達成バッジを付与: {user.username} ({today_movie_count}本)")

    #「３ジャンルの映画鑑賞達成」のミッション
    success, message = MissionService.check_and_assign_genre_batch(user)
    if success:
        print(f"3ジャンル制覇バッジを付与 ユーザー: {user.username} - {message}")
    else:
        print(f"3ジャンル未達成ユーザー: {user.username} - {message}")
