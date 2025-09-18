from django.test import TestCase
from django.urls import reverse,resolve
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Recommend_SelectTests(TestCase):
    #　作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
    
    # 気分選択画面のURL逆引き、ルーティングが適切である確認
    def test_reverse_and_resolve(self):
        url = reverse("movies:recommend_select")
        self.assertEqual(url, "/movies/recommend/")

        resolver_match= resolve("/movies/recommend/")
        self.assertEqual(resolver_match.view_name, "movies:recommend_select")

    # ログイン済みユーザーが感情選択画面にアクセスでき、期待テンプレートで描画されることを確認
    def test_status_and_template(self):
        self.client.login(username = "u", password = "p")
        response = self.client.get(reverse("movies:recommend_select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/recommend_select.html")

    # 未ログインならLOGIN_URLにリダイレクト
    def test_redirects_when_not_logged_in(self):
        path = reverse("movies:recommend_select")
        response = self.client.get(path)

        expected_url = f"{resolve_url(settings.LOGIN_URL)}?next={path}"
        self.assertRedirects(response, expected_url)