from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeViewTests(TestCase):
    # 作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")

    # ユーザーがログインした際にホーム画面にアクセスできることの確認
    def test_access_when_logged_in(self):
        self.client.login(username="u", password="p")
        res = self.client.get(reverse("movies:home"))
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,"movies/home.html")