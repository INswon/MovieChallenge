import requests
from decouple import config

# 環境変数からAPIキーの取得
TMDB_API_KEY = config("TMDB_API_KEY")  
BASE_URL = "https://api.themoviedb.org/3/"

# おすすめ映画表示フィルター設定
BASE_PARAMS = {
    "language": "ja-JP",                # 取得言語(日本語)
    "region": "JP",                     # 日本の公開/人気を優先
    "include_adult": "false",           # 成人向けカテゴリ除去
    "primary_release_date.gte": "1990-01-01",  # 1990年以降の映画を対象
    "sort_by": "popularity.desc",       # 人気順にソート（代表作が上に来やすい）
    "vote_count.gte": 500,              # 評価数500以上 → マイナー作品を除外
}

# 感情カテゴリーとジャンルのマッピング
MOOD_TO_GENRES = {
    "癒された": [10751,16],        # ファミリー、アニメーション
    "泣いた": [18,10749],          # ドラマ、ロマンス
    "興奮した": [12,14,28],        # アドベンチャー、ファンタジー、アクション
    "怖かった": [27,53],            # ホラー、スリラー
    "新鮮だった": [9648,878,99],   # ミステリー、SF、ドキュメンタリー
}


# TMDb API から映画データ取得するサービス
class TmdbMovieService:

    # おすすめ映画のあらすじ表示を80文字に制限
    @staticmethod
    def truncate_text(text, max_length=80):
        #　文章がない時 (空文字を返す)
        if text is None or text =="":
            return ""
        
        # 80文字以下の時 (そのまま表示)
        if len(text) <= max_length:
            return text
        
        # 80文字以上の時 (…を末尾につける)
        long_text = text[:max_length]
        return long_text + "…" 

    # 代表作5作品の取得
    @staticmethod
    def discover_top5(genre_id=None):
        url = f"{BASE_URL}discover/movie"
        params = {**BASE_PARAMS, "api_key": TMDB_API_KEY}
        if genre_id:
            params["with_genres"] = genre_id

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            results = response.json().get("results", [])
            items = results[:5]  

            formatted = []
            for m in items:
                formatted.append({
                    "id": m.get("id"),
                    "title": m.get("title"),
                    "overview": TmdbMovieService.truncate_text(m.get("overview"), 80),
                    "poster_url": (
                        f"https://image.tmdb.org/t/p/w342{m['poster_path']}"
                        if m.get("poster_path") else None
                    ),
                    "rating": m.get("vote_average"),
                })
            return formatted
        except requests.exceptions.RequestException as e:
            print(f"[Discover取得] APIエラー: {e}")
            return []

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
