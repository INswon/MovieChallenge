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

    @staticmethod
    def get_movie_detail(movie_id):
        url = f"{BASE_URL}movie/{movie_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ja-JP"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[詳細取得] APIエラー: {e}")
            return None
        

    @staticmethod
    def get_director_name(movie_id):
        url = f"{BASE_URL}movie/{movie_id}/credits"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ja-JP"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            for crew_member in data.get("crew", []):
                if crew_member.get("job") == "Director":
                    return crew_member.get("name")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[監督取得] APIエラー: {e}")
            return None

    @staticmethod
    def get_movie_info(movie_id):
        detail = TmdbMovieService.get_movie_detail(movie_id)
        director = TmdbMovieService.get_director_name(movie_id)

        if not detail:
            return None

        return {
            "title": detail.get("title"),
            "poster_url": (
                f"https://image.tmdb.org/t/p/w200{detail.get('poster_path')}"
                if detail.get("poster_path") else None
            ),
            "genres": [g["name"] for g in detail.get("genres", [])],
            "director": director
        }
