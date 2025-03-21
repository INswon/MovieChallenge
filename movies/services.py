from django.http import JsonResponse
from django.views import View
import requests
from decouple import config

#環境変数からAPIキーの取得()
TMDB_API_KEY = config('TMDB_API_KEY')  
TMDB_ACCESS_TOKEN = config('TMDB_ACCESS_TOKEN')
BASE_URL = "https://api.themoviedb.org/3/"

#映画タイトルを検索するクラスベースビュー
class MovieSerchView(View):
    def get(self, request, *args, **kwargs):
        query = request.get("query")
        if not query:
            return JsonResponse({"error":"検索ワードを入力してください"}, status=400)
        
        url = f"{BASE_URL}search/movie"
        params = {
            "api_key": TMDB_API_KEY,  
            "query": query,
            "language": "ja-JP"
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            movies = response.json().get("results", [])

            return JsonResponse({"movies": movies}, status=200)
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": f"APIエラー: {e}"}, status=500)
