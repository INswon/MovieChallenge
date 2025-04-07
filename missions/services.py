from movies.models import UserMovieRecord,Genre
from missions.models import Mission, UserMission, UserBatch, Batch
from django.utils.timezone import now

# ミッション達成判定に使用する対象ジャンルのリスト
TARGET_GENRE_NAMES = [
    "アクション", "アドベンチャー", "SF",
    "ミステリー", "恋愛", "コメディ",
    "ファンタジー", "サスペンス", "ファンタジー", "アドベンチャー",
    "ドラマ","ロマンス",
]

class MissionService:

    #「3本の映画視聴達成」のミッションバッジ付与処理
    @staticmethod
    def check_and_complete_mission(user, mission_title):
        mission = Mission.objects.filter(title=mission_title).first()
        
        if not mission:
            print(f"ミッション '{mission_title}' が存在しませんでした")
            return False, "ミッションが見つかりませんでした"

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
        mission = Mission.objects.filter(title=mission_title).first()
        if not mission:
            print(f"ミッション '{mission_title}' が存在しませんでした")
            return

        user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)
        if not user_mission.is_completed:
            user_mission.is_completed = True
            user_mission.completed_at = now()
            user_mission.save()

        if mission.batch:
            UserBatch.objects.get_or_create(user=user, batch=mission.batch)


    # 映画の記録ジャンルが3種類以上なら「3ジャンル制覇」バッジを付与
    @staticmethod
    def check_and_assign_genre_batch(user):
        mission = Mission.objects.filter(title="3ジャンル制覇").first()
        if not mission:
            print("３ジャンル制覇ミッションが存在しませんでした")
            return False, "ミッションが存在しません"


        user_genres = Genre.objects.filter(
            usermovierecord__user=user,
            usermovierecord__is_deleted=False
        ).distinct()

        matched_genres = [
            genre.name for genre in user_genres
            if genre.name in TARGET_GENRE_NAMES
        ]

        if len(set(matched_genres)) >= 3:
            user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)

            if user_mission.is_completed:
                return False, "すでにこのミッションを達成済みです"
            
            user_mission.is_completed = True
            user_mission.completed_at = now()
            user_mission.save()

            if mission.batch:
                UserBatch.objects.get_or_create(user=user, batch=mission.batch)

            return True, "ミッションを達成しました！"

        return False, "まだ対象ジャンルが3種類に到達していません"
