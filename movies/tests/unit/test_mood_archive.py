from django.test import TestCase
from django.contrib.auth.models import User
from movies.models import Mood
from django.urls import reverse

# 感情アーカイブページの遷移に関するテストケース
class MoodPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.mood = Mood.objects.create(name="癒された")

    # (正常系) 感情名「癒された」でアクセスした場合、200が返る
    def test_mood_page_returns_200(self):
        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # (異常系) 存在しない感情名でアクセスした場合、404が返る
    def test_mood_page_returns_404_for_invalid_id(self):
        url = reverse("movies:mood_archive", kwargs={"mood_name": "存在しない感情"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
