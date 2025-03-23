import requests
from decouple import config

# 環境変数からAPIキーの取得
TMDB_API_KEY = config("TMDB_API_KEY")  
BASE_URL = "https://api.themoviedb.org/3/"

# TMDb API から映画データ取得するサービス
class TmdbMovieService:

    @staticmethod
    def search(query):
        if not query:
            return []

        url = f"{BASE_URL}search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": query,
            "language": "ja-JP"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(f"APIレスポンス: {data}") 
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"APIエラー: {e}")
            return []
