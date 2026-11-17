from unittest.mock import patch, Mock
from django.test import SimpleTestCase
from movies.services import TmdbMovieService, TMDB_API_KEY 

class TmdbMovieServiceTests(SimpleTestCase):

    def setUp(self):
        self.service = TmdbMovieService()
        self.expected_url = (
            "https://api.themoviedb.org/3/discover/movie"
        )

    # APIのリクエスト先URLが一致していることの検証
    @patch("movies.services.requests.get")
    def test_request_url_is_correct(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        self.service.discover_top5()

        actual_url = mock_get.call_args.args[0]
        self.assertEqual(actual_url, self.expected_url)

    #　APIキーの送信ができていることの検証
    @patch("movies.services.requests.get")
    def test_request_key_is_correct(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        expected_api_key = TMDB_API_KEY

        self.service.discover_top5()

        # MockのリクエストからAPIキーの取得
        actual_params = mock_get.call_args.kwargs["params"]
        actual_api_key = actual_params["api_key"]

        self.assertEqual(actual_api_key, expected_api_key)

    # ジャンルIDの送信ができていることの検証
    @patch("movies.services.requests.get")
    def test_request_genre_params_are_correct(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        expected_genre_ids = "10751|16"

        self.service.discover_top5([10751, 16])

        # Mockのリクエストからパラメータを取得
        actual_params = mock_get.call_args_list[1].kwargs["params"]
        actual_genre_ids = actual_params["with_genres"]

        self.assertEqual(actual_genre_ids, expected_genre_ids)

    # ジャンルIDの返却値が適切か検証
    @patch("movies.services.requests.get")
    def test_movie_search_uses_get_request(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        self.service.discover_top5([10751, 16])

        # discover_top5内でGETリクエストが実行されたことを確認
        self.assertTrue(mock_get.called)

    # 映画検索APIに渡す検索パラメータが仕様どおりか検証
    @patch("movies.services.requests.get")
    def test_search_parameters_are_correct(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # 期待する検索条件
        expected_params = {
            "language": "ja-JP",
            "region": "JP",
            "include_adult": "false",
            "primary_release_date.gte": "1990-01-01",
            "sort_by": "popularity.desc",
            "vote_count.gte": 500,
        }

        self.service.discover_top5()
        actual_parmas = mock_get.call_args.kwargs["params"]

        for key, expected_value in expected_params.items():
            self.assertEqual(actual_parmas[key], expected_value)
