from django.test import TestCase
from django.urls import reverse, resolve
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model
from django.conf import settings
from movies.constants import RECOMMEND_CATEGORY, RECOMMEND_MOVIE
from movies.services import MOOD_TO_GENRES
from unittest.mock import patch

User = get_user_model()
ANY_VALID = next(iter(RECOMMEND_CATEGORY.keys()))

# listなら"|"連結、strならそのまま
def join_or_keep(v):
    return v if isinstance(v, str) else "|".join(map(str, v))

class Recommend_ListTests(TestCase):
    #　作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
     
    # 気分別おすすめ映画一覧のURL逆引き、ルーティングが適切である確認　
    def test_reverse_and_resolve(self):
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend", args=[key])
            match = resolve(url)

            self.assertEqual(match.view_name, "movies:recommend")
            self.assertEqual(match.kwargs, {"category":key})

    # ログイン済みユーザーが気分別おすすめ映画一覧にアクセスでき、期待テンプレートで描画されることを確認　
    def test_status_and_template(self):
        self.client.login(username = "u", password = "p")
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend", args=[key])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "movies/recommend_list.html")

    # 未ログインユーザーはリダイレクトされることの確認　
    def test_redirects_when_not_logged_in(self):
        for key in RECOMMEND_CATEGORY.keys():
            path = reverse("movies:recommend", args=[key])
            response = self.client.get(path)

            expected_url = f"{resolve_url(settings.LOGIN_URL)}?next={path}"
            self.assertRedirects(response, expected_url)
        
    # 見出しはカテゴリー別の日本語ラベルが出る（全カテゴリ）
    def test_heading_shows_category_label(self):
        self.client.login(username="u", password="p")
        for key, category_data in RECOMMEND_CATEGORY.items():
            url = reverse("movies:recommend", args=[key])
            response = self.client.get(url)
            expected_heading = f"「{category_data['label']}」おすすめの作品はこちら"
            self.assertContains(response, expected_heading)
    
    # 各カテゴリの映画タイトル,内容が全件表示されることの確認 
    def test_all_movie_titles_render(self):
        self.client.login(username="u", password="p")
        for key in RECOMMEND_CATEGORY.keys():
            url = reverse("movies:recommend", args=[key])
            response = self.client.get(url)
            for mv in RECOMMEND_MOVIE[key]:
                self.assertContains(response, mv["title"])
                self.assertContains(response, mv["note"])

    # 存在しないcategoryを指定時、サーバ内部エラー(500)ではなく、リソース不在を表すHTTP 404を返すことの確認
    def test_invalid_category_returns_404(self):
        self.client.login(username="u", password="p")  
        url = reverse("movies:recommend", args=["__invalid__"])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    #　正しいジャンルIDでサービス呼び出しが行われているかの確認
    @patch("movies.views.TmdbMovieService.discover_top5")  
    def test_view_calls_service_with_correct_with_genres(self, mock_discover):
        self.client.login(username="u", password="p")  
        mock_discover.return_value = [{
            "title": "dummy",
            "overview": "dummy",
            "poster_url": None,   
            "genres": [],         
            "rating": 3.5         
        }]

        url = reverse("movies:recommend", args=[ANY_VALID])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # 呼び出し確認
        mock_discover.assert_called_once()

        # 期待値：配列は"|"連結、文字列はそのまま
        expected = join_or_keep(MOOD_TO_GENRES[ANY_VALID])

        # 位置/キーワード 両対応で取得（今回は位置引数対策）
        args, kwargs = mock_discover.call_args
        passed = kwargs.get("with_genres") or (args[0] if args else None)

        self.assertEqual(passed, expected)