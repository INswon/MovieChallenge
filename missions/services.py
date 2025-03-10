from movies.models import UserMovieRecord
from missions.models import Mission, UserMission, UserBatch, Batch
from django.utils.timezone import now

class MissionService:
    @staticmethod
    def check_and_complete_mission(user, mission_title):
        mission = Mission.objects.get(title=mission_title)
        watched_movies_count = UserMovieRecord.objects.filter(user=user, is_deleted=False).count()

        if watched_movies_count >= 3:
            user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)

            if created or not user_mission.is_completed:
                user_mission.is_completed = True
                user_mission.completed_at = now()
                user_mission.save()

            MissionService.grant_batch_for_mission(user, mission_title)
            return True, "ミッションを達成しました！"

        return False, "まだミッション達成に必要な視聴数に到達していません"

    @staticmethod
    def grant_batch_for_mission(user, mission_title):
        mission = Mission.objects.get(title=mission_title)
        user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)
        if not user_mission.is_completed:
            user_mission.is_completed = True
            user_mission.completed_at = now()
            user_mission.save()

        if mission.batch:
            UserBatch.objects.get_or_create(user=user, batch=mission.batch)
