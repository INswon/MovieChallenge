from movies.models import UserMovieRecord
from missions.models import Mission, UserMission, UserBatch
from django.utils.timezone import now
import logging

logger = logging.getLogger('missions') 

#ミッション完了処理の設定
class MissionCompletionHandler:
    @staticmethod
    #ミッションを達成した場合、ユーザーにバッチを付与する処理
    def assign_batch(user, mission_title):

        mission = Mission.objects.get(title=mission_title)
        success, message = MissionCompletionHandler.complete_mission(user, mission)

        if success and mission.batches.exists():
            for batch in mission.batches.all():
                UserBatch.objects.get_or_create(user=user, batch=batch)

        return success, message

#ミッション管理サービス
class MissionService:
    @staticmethod
    # 指定されたミッションの達成条件を満たしているかを確認し、達成処理を行う
    def check_and_complete_mission(user, mission_title):
        
        mission = Mission.objects.get(title=mission_title)

        watched_movies_count = UserMovieRecord.objects.filter(user=user, is_deleted=False).count()

        if watched_movies_count >= 3:
            print("Condition met for mission completion.")
            print(f"UserMission before processing: {UserMission.objects.filter(user=user, mission=mission)}")
    
            user_mission, created = UserMission.objects.get_or_create(user=user, mission=mission)
            print(f"UserMission retrieved or created: {user_mission}, Created: {created}")

            if not user_mission.is_completed:
                user_mission.is_completed = True
                user_mission.completed_at = now()
                user_mission.save()
                print(f"UserMission updated: {user_mission}")
                return True, "ミッションを達成しました！"
            else:
                print("UserMission already completed.")
                return False, "まだミッション達成に必要な視聴数に到達していません"
            

    @staticmethod
    #ミッションが達成された場合に、バッチを付与する処理
    def grant_batch_for_mission(user, mission_title):
        logger.debug(f"grant_batch_for_mission() 実行: {mission_title}, User: {user.username}")
        print(f"grant_batch_for_mission() 実行: {mission_title}, User: {user.username}")  

        success, message = MissionService.check_and_complete_mission(user, mission_title)

        if success:
            mission = Mission.objects.get(title=mission_title)
            logger.debug(f"バッチ付与処理実行: {mission}")
            print(f"バッチ付与処理実行: {mission}") 

            if mission.batch:
                logger.debug(f"付与対象バッチ: {mission.batch}")
                print(f"付与対象バッチ: {mission.batch}")  
                user_batch, created = UserBatch.objects.get_or_create(user=user, batch=mission.batch)
                logger.info(f"バッチ付与完了: {user_batch.batch.name}, Created: {created}")
                print(f"バッチ付与完了: {user_batch.batch.name}, Created: {created}")  
            else:
                logger.warning("ミッションにバッチが設定されていません！")
                print("ミッションにバッチが設定されていません！")  
                
        return message
