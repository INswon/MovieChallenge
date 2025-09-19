from django.test import TestCase
from django.urls import reverse, resolve
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from django.conf import settings
from movies.constants import RECOMMEND_CATEGORY

User = get_user_model()
class Recommend_ListTests(TestCase):
    #　作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
     
    # 気分別おすすめ映画一覧のURL逆引き、ルーティングが適切である確認
    def test_reverse_and_resolve(self):
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend_list", args=[key])
            match = resolve(url)

            self.assertEqual(match.view_name, "movies:recommend_list")
            self.assertEqual(match.kwargs, {"category":key})

    # ログイン済みユーザーが気分別おすすめ映画一覧にアクセスでき、期待テンプレートで描画されることを確認
    def test_status_and_template(self):
        self.client.login(username = "u", password = "p")
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend_list", args=[key])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "movies/recommend_list.html")

    # 未ログインユーザーはリダイレクトされることの確認
    def test_redirects_when_not_logged_in(self):
        for key in RECOMMEND_CATEGORY.keys():
            path = reverse("movies:recommend_list", args=[key])
            response = self.client.get(path)

            expected_url = f"{resolve_url(settings.LOGIN_URL)}?next={path}"
            self.assertRedirects(response, expected_url)
        
    # 見出しはカテゴリー別の日本語ラベルが出る（全カテゴリ）
    def test_heading_shows_category_label(self):
        self.client.login(username="u", password="p")
        for key, category_data in RECOMMEND_CATEGORY.items():
            url = reverse("movies:recommend_list", args=[key])
            response = self.client.get(url)
            expected_heading = f"「{category_data['label']}」おすすめの作品はこちら"
            self.assertContains(response, expected_heading)