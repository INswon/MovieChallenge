from django.test import TestCase
from django.urls import reverse,resolve

class Recommend_SelectTests(TestCase):
    
    # 気分選択画面のURL逆引き、ルーティングが適切である確認
    def test_reverse_and_resolve(self):
        url = reverse("movies:recommend_select")
        self.assertEqual(url, "/movies/recommend/")

        resolver_match= resolve("/movies/recommend/")
        self.assertEqual(resolver_match.view_name, "movies:recommend_select")