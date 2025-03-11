import io
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse
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

class TestMissionView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        # 「3本の映画達成」バッジ & ミッション
        self.batch_3_movies = Batch.objects.create(
            name="3本の映画達成バッジ", 
            description="3本の映画を視聴達成",
            icon=create_dummy_image()
        )
        
        self.mission_3_movies = Mission.objects.create(
            title="3本の映画達成",
            description="3本の映画を視聴する。",
            criteria={"min_watch_count": 3},
            batch=self.batch_3_movies,
        )

        # 「1日3本の映画視聴達成」バッジ & ミッション
        self.batch_3_movies_day = Batch.objects.create(
            name="1日3本の映画視聴達成バッジ", 
            description="1日に3本の映画を視聴達成",
            icon = create_dummy_image()
        )

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

    #"映画が2本以下のとき、ミッションは未達成の検証
    def test_missions_not_completed_before_3_movies(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("missions:user_batch_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json") 
