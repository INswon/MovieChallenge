from django.test import TestCase
from django.urls import reverse, resolve

class Recommend_ListTests(TestCase):
    # 気分別おすすめ映画一覧のURL逆引き、ルーティングが適切である確認
    def test_reverse_and_resolve(self):
        url = reverse("movies:recommend_list", kwargs={"category": "energy"})
        self.assertEqual(url, "/movies/recommend/energy/")

        match= resolve("/movies/recommend/energy/")
        self.assertEqual(match.view_name, "movies:recommend_list")
        self.assertEqual(match.kwargs, {"category":"energy"})
