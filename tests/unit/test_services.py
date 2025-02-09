from django.test import TestCase
from django.contrib.auth.models import User
from missions.models import Mission, UserBatch, UserMission, Batch
from movies.models import UserMovieRecord
from missions.services import MissionService

class MissionServiceTestCase(TestCase):
    def setUp(self):
        # テストユーザー作成
        self.user = User.objects.create_user(username="kouji", password="password")

        # テスト用ミッション作成
        self.mission = Mission.objects.create(
            title="3本の映画達成",
            description="映画を3本見る",
            criteria={"watched_movies_count": 3}  # ミッション条件を指定
        )

        # テスト用バッチ作成とミッションへの紐付け
        self.batch = Batch.objects.create(
            name="3本の映画達成バッチ",
            description="映画を3本視聴しました！",
            mission=self.mission  # 関連するミッションを指定
        )

        # テスト用映画視聴記録作成
        UserMovieRecord.objects.create(user=self.user, title="Movie 1", date_watched="2024-01-01")
        UserMovieRecord.objects.create(user=self.user, title="Movie 2", date_watched="2024-01-02")
        UserMovieRecord.objects.create(user=self.user, title="Movie 3", date_watched="2024-01-03")


    def test_grant_batch_for_mission(self):
        # バッチ付与処理を実行
        MissionService.grant_batch_for_mission(self.user, "3本の映画達成")

        # UserBatch にデータが作成されているか確認
        user_batches = UserBatch.objects.filter(user=self.user)
        print(f"UserBatches: {list(user_batches)}")  # デバッグ用出力

        self.assertEqual(user_batches.count(), 1)

        # 付与されたバッチが正しいか確認
        batch = user_batches.first().batch
        print(f"Batch Name: {batch.name}")  # デバッグ用出力
        self.assertEqual(batch.name, "3本の映画達成バッチ")
