from unittest.mock import patch, Mock
from django.test import SimpleTestCase
from movies.services import TmdbMovieService


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
