import io
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from movies.models import UserMovieRecord
from missions.models import Mission, UserMission, Batch, UserBatch
from django.core.files.base import ContentFile
from django.db import transaction
import missions.signals

User = get_user_model()

def create_dummy_image():
    image = Image.new("RGB", (1, 1), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name="test_poster.jpg")

class TestMissionSignals(TestCase):
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

    #「3本の映画達成」ミッションを満たした時の検証
    def test_mission_created_after_3_movies(self):
        today = now().date()
        def check_mission_created():
            self.assertTrue(
                UserMission.objects.filter(user=self.user, mission=self.mission_3_movies_day).exists(),
                "映画3本視聴でミッションが作成されることを確認"
            )

        #トランザクション完了後にシグナルの発火を待ち、ミッションが作成されることを確認
        transaction.on_commit(check_mission_created)
        UserMovieRecord.objects.create(user=self.user, title="Movie 1", date_watched=today, rating="5")
        UserMovieRecord.objects.create(user=self.user, title="Movie 2", date_watched=today, rating="5")
        UserMovieRecord.objects.create(user=self.user, title="Movie 3", date_watched=today, rating="5")

    #「1日３本の映画視聴達成」ミッションを満たした時の検証
    def test_mission_created_after_watching_3_movies_in_one_day(self):
        today = now().date()

        def check_mission_created():
            self.assertTrue(
                UserMission.objects.filter(user=self.user, mission=self.mission_3_movies_day).exists(),
                "1日3本視聴でミッションが作成されることを確認"
            )
        
        # トランザクション完了後にミッション作成を確認
        transaction.on_commit(check_mission_created)
        UserMovieRecord.objects.create(user=self.user, title="Movie A", date_watched=today, rating="5")
        UserMovieRecord.objects.create(user=self.user, title="Movie B", date_watched=today, rating="5")
        UserMovieRecord.objects.create(user=self.user, title="Movie C", date_watched=today, rating="5")
