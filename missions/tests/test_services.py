import io
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils import timezone
from movies.models import UserMovieRecord
from missions.models import Mission, UserMission, Batch, UserBatch
from missions.services import MissionService
from PIL import Image
from django.core.files.base import ContentFile
from django.db import transaction

User = get_user_model()

def create_dummy_image():
    image = Image.new("RGB", (1, 1), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name="test_poster.jpg")

class TestMissionService(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        # 「3本の映画達成」バッジ & ミッション
        self.batch_3_movies = Batch.objects.create(name="3本の映画達成バッジ", description="3本の映画を視聴達成")
        self.mission_3_movies = Mission.objects.create(
            title="3本の映画達成",
            description="3本の映画を視聴する。",
            criteria={"min_watch_count": 3},
            batch=self.batch_3_movies
        )

        # 「1日3本の映画視聴達成」バッジ & ミッション
        self.batch_3_movies_day = Batch.objects.create(name="1日3本の映画視聴達成バッジ", description="1日に3本の映画を視聴達成")
        self.mission_3_movies_day = Mission.objects.create(
            title="1日3本の映画視聴達成",
            description="1日で3本の映画を視聴する。",
            criteria={"min_watch_count": 3, "same_day": True},
            batch=self.batch_3_movies_day
        )

        today = now().date()
        UserMovieRecord.objects.bulk_create([
            UserMovieRecord(user=self.user, title="Movie 1", date_watched=today, rating="5", poster=create_dummy_image()),
            UserMovieRecord(user=self.user, title="Movie 2", date_watched=today, rating="5", poster=create_dummy_image()),
            UserMovieRecord(user=self.user, title="Movie 3", date_watched=today, rating="5", poster=create_dummy_image()),
        ])

    #「3本の映画達成」ミッションを満たした時の検証
    def test_mission_is_completed_when_3_movies_watched(self):
        with transaction.atomic():
            self.assertFalse(UserMission.objects.filter(user=self.user, mission=self.mission_3_movies).exists(), "事前に UserMission が作成されていないことを確認してください")
            success, message = MissionService.check_and_complete_mission(self.user, self.mission_3_movies.title)
            self.assertTrue(success, "ミッション達成フラグが True である必要があります")
            self.assertEqual(message, "ミッションを達成しました！", "ミッション達成時のメッセージが期待値と異なります")
            self.assertTrue(UserMission.objects.filter(user=self.user, mission=self.mission_3_movies).exists(), "UserMission が正しく作成されていることを確認してください")
            self.assertTrue(UserBatch.objects.filter(user=self.user, batch=self.batch_3_movies).exists(), "ミッション達成後にバッジが正しく付与されていることを確認してください")

    #「1日３本の映画視聴達成」ミッションを満たした時の検証
    def test_mission_created_after_watching_3_movies_in_one_day(self):
        with transaction.atomic():
            self.assertFalse(UserMission.objects.filter(user=self.user, mission=self.mission_3_movies_day).exists(), "事前に UserMission が作成されていないことを確認してください")
            success, message = MissionService.check_and_complete_mission(self.user, self.mission_3_movies_day.title)
            self.assertTrue(success, "ミッション達成フラグが True である必要があります")
            self.assertEqual(message, "ミッションを達成しました！", "ミッション達成時のメッセージが期待値と異なります")
            self.assertTrue(UserMission.objects.filter(user=self.user, mission=self.mission_3_movies_day).exists(), "UserMission が正しく作成されていることを確認してください")
            self.assertTrue(UserBatch.objects.filter(user=self.user, batch=self.batch_3_movies_day).exists(), "ミッション達成後にバッジが正しく付与されていることを確認してください")
