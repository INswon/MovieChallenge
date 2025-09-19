from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from movies.constants import RECOMMEND_CATEGORY

User = get_user_model()
class Recommend_ListTests(TestCase):
    #　作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
     
    # 気分別おすすめ映画一覧のURL逆引き、ルーティングが適切である確認
    def test_reverse_and_resolve(self):
        url = reverse("movies:recommend_list", kwargs={"category": "energy"})
        self.assertEqual(url, "/movies/recommend/energy/")

        match= resolve("/movies/recommend/energy/")
        self.assertEqual(match.view_name, "movies:recommend_list")
        self.assertEqual(match.kwargs, {"category":"energy"})

    # ログイン済みユーザーが気分別おすすめ映画一覧にアクセスでき、期待テンプレートで描画されることを確認
    def test_status_and_template(self):
        self.client.login(username = "u", password = "p")
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend_list", args=[key])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "movies/recommend_list.html")
    
    