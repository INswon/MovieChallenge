from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeViewTests(TestCase):
    # 作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")

    # ユーザーがログインした際にホーム画面にアクセスできることの確認
    def test_access_when_logged_in(self):
        self.client.login(username="u", password="p")
        response = self.client.get(reverse("movies:home"))

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "movies/home.html")
    
    # 未ログインユーザーがホーム画面にアクセスした時LOGIN_URLにリダイレクトされることの確認
    def test_redirects_when_not_logged_in(self):
        path = reverse("movies:home")
        response =  self.client.get(path)

        expected_url = f"{resolve_url(settings.LOGIN_URL)}?next={path}"
        self.assertRedirects(response, expected_url)

    # 「気分を選んでおすすめを見る」ボタンを押して、映画推薦画面に画面遷移することの検証
    def test_main_cta_navigates_to_recommend_page(self):
        self.client.login(username="u", password="p")
        path = reverse("movies:home")
        recommend_path = reverse("movies:recommend", kwargs={"recommend_name": "healed"})

        response = self.client.get(path)
        self.assertContains(response, 'data-testid="recommend"')
        self.assertContains(response, f'href="{recommend_path}"')
        resp2 = self.client.get(recommend_path)

        self.assertEqual(resp2.status_code, 200)
        self.assertTemplateUsed(resp2, "movies/recommend.html")
