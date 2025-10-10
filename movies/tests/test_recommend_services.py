from django.test import TestCase
from unittest.mock import patch, Mock
from movies.services import TmdbMovieService as tmdb, MOOD_TO_GENRES

class TmdbServiceParamTests(TestCase):

    # 主要なパラメータ（言語・地域・年・成人除外・人気順・評価数500以上・ジャンル指定）が揃っていること
    @patch("movies.services.requests.get")
    def test_all_base_params_are_included(self, mock_get):

        # モックの設定 (API呼び出しが成功したかのように振る舞わせる)
        mock_get.return_value = Mock(status_code=200, json=lambda: {"results": []})
        
        # 実行: 怖いジャンルID（[27, 53]）を直接渡してサービスを呼び出す
        tmdb.discover_top5([27, 53]) 

        # 呼び出し履歴から with_genres=27|53 の discover/movie 呼び出しを1件探す
        found_correct_call = False
        params = None
        for args, kwargs in mock_get.call_args_list:
            url = args[0] if args else kwargs.get("url")
            if not url:
                continue
            if url.endswith("/discover/movie"):
                cand = kwargs.get("params", {})
                if cand.get("with_genres") == "27|53":
                    params = cand
                    found_correct_call = True
                    break

        # 最低1回は条件を満たす呼び出しがあること
        self.assertTrue(found_correct_call, "with_genres=27|53 を含むAPI呼び出しが見つかりませんでした。")

        # 該当呼び出しのパラメータを検証
        expected = {
            "language": "ja-JP", # 言語
            "region": "JP", # 地域
            "include_adult": "false", # 成人除外
            "sort_by": "popularity.desc", # 人気順
            "with_genres": "27|53", 
        }
        for k, v in expected.items():
            self.assertEqual(params.get(k), v)

        # 評価件数・公開年パラメータ
        self.assertGreaterEqual(int(params["vote_count.gte"]), 500)
        self.assertIn("primary_release_date.gte", params)

    # 感情カテゴリー(MOOD_TO_GENRES)キーに差異がないことの確認
    def test_mood_keys_exact(self):
        expected = {"healing","impression","energy","scary","curious"}

        actual = set(MOOD_TO_GENRES.keys())

        missing = expected - actual
        extra   = actual - expected
        assert actual == expected, f"Missing: {sorted(missing)} / Extra: {sorted(extra)}"
    
    # id, タイトル, あらすじ, ジャンルID, 評価が適切であること
    @patch("movies.services.TmdbMovieService._genre_map", return_value={27: "Horror", 53: "Thriller"})
    @patch("movies.services.TmdbMovieService.truncate_text", return_value="TRIMMED_80")
    @patch("movies.services.requests.get")
    def test_parameters_returns(self, mock_get, mock_trunc, mock_gmap): 
        # モックでAPIの戻り値を定義
        mock_data = {
            "results": [
            {
                "id": 1259,
                "title": "リング",
                "overview": "ジャーナリストの浅川和美は、姪の突然の死を追ううちに、見た者は1週間後に死ぬという「呪いのビデオ」の存在を知る。彼女自身もビデオを見てしまい、残された時間を呪いの謎を解明するために奔走する。",
                "poster_path": "/5N90Qv2K8eNf1x0v9Q9sE1wYx7X.jpg",
                "genre_ids": [27, 53],
                "vote_average": 7.3,
                "release_date": "1998-01-31"
            }
        ]
    }
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_data)

        # 関数呼び出し（services.py 内の対象）
        out = tmdb.discover_top5([27, 53])

        #　期待される変換後データ
        expected = [
            {
                "id": 1259,
                "title": "リング",
                "overview": "TRIMMED_80",  
                "poster_url": "https://image.tmdb.org/t/p/w342/5N90Qv2K8eNf1x0v9Q9sE1wYx7X.jpg",
                "genres": ["Horror", "Thriller"],  
                "rating": 3.6,  
            }
        ]

        # 比較（完全一致）
        assert out == expected
    
    # おすすめ映画データ未取得時、空リスト([])を返すことの確認
    @patch("movies.services.requests.get")
    def test_return_empty_when_no_results(self,mock_get):

        # APIが「空のresults」を返すシナリオをモックで作成
        mock_get.return_value = Mock(status_code=200, json=lambda:{"results": []})

        # おすすめ映画呼び出し(discover_top5)を実行
        out = tmdb.discover_top5([27, 53])

        # 例外を発生させず、空リスト([])を返すことを確認
        assert out == []