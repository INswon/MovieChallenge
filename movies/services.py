import requests, random, logging
from decouple import config

logger = logging.getLogger(__name__)

# 準備: 環境変数からAPIキーの取得
TMDB_API_KEY = config("TMDB_API_KEY")  
BASE_URL = "https://api.themoviedb.org/3/"

# 映画推薦機能 (ページ取得の制御定数)
START_PAGE = 1
MAX_PAGE = 30
PAGES_PER_FETCH = 3 # 1〜30ページの中の3ページを検索対象にする

# 映画推薦機能 (おすすめ映画表示フィルター設定)
BASE_PARAMS = {
    "language": "ja-JP",                # 取得言語(日本語)
    "region": "JP",                     # 日本の公開/人気を優先
    "include_adult": "false",           # 成人向けカテゴリ除去
    "primary_release_date.gte": "1990-01-01",  # 1990年以降の映画を対象
    "sort_by": "popularity.desc",       # 人気順にソート（代表作が上に来やすい）
    "vote_count.gte": 500,              # 評価数500以上 → マイナー作品を除外
}

# 映画推薦機能 (感情カテゴリーとジャンルのマッピング)
MOOD_TO_GENRES = {
    "healing": [10751,16],        # ファミリー、アニメーション
    "impression": [18,10749],          # ドラマ、ロマンス
    "energy": [12,28],        # アドベンチャー、アクション
    "scary": [27,53],            # ホラー、スリラー
    "curious": [9648,878,99],   # ミステリー、SF、ドキュメンタリー
}

# TMDb API から映画データ取得するサービス
class TmdbMovieService:

    # 映画推薦機能 (おすすめ映画のあらすじ表示を80文字に制限)
    @staticmethod
    def truncate_text(text, max_length=80):
        if text is None or text =="":
            return ""
        
        if len(text) <= max_length:
            return text
        
        long_text = text[:max_length]
        return long_text + "…"

    # ジャンル辞書の取得 
    @staticmethod
    def _genre_map():
        url = f"{BASE_URL}genre/movie/list"
        params = {"api_key": TMDB_API_KEY, "language": "ja-JP"}
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        return {g["id"]: g["name"] for g in r.json().get("genres", [])}

    # 映画推薦機能 (代表作5作品の取得)

    @staticmethod
    def get_safe_genre_ids(category):
        genre_ids = MOOD_TO_GENRES.get(category)
        
        if genre_ids is None:
            logger.warning(f"[CATEGORY_NOT_FOUND] Category '{category}' is not defined in MOOD_TO_GENRES.")
            return [] 
            
        return genre_ids
        
    @staticmethod
    def discover_top5(genre_ids=None):

        url = f"{BASE_URL}discover/movie"
        
        # 1. 引数の安全な処理: どんな型が来てもTMDB用の文字列「10|12」に変換
        if not genre_ids:
            with_genres = ""
        elif isinstance(genre_ids, list):
            with_genres = "|".join(map(str, genre_ids))
        else:
            # 文字列や単一の数値が来ても動作を保証する
            with_genres = str(genre_ids)

        logger.info(f"[TMDB_FETCH] Start fetching movies. genres='{with_genres}'")

        # 2. ジャンルマップの取得 (ここが失敗しても空リストで耐える)
        try:
            gmap = TmdbMovieService._genre_map()
        except Exception as e:
            logger.error(f"[TMDB_ERROR] Failed to fetch genre map: {e}")
            return []

        # 3. 検索対象ページのサンプリング
        pages = random.sample(range(START_PAGE, MAX_PAGE + 1), k=PAGES_PER_FETCH)
        pool, seen_ids = [], set()

        # 4. APIリクエストループ
        for p in pages:
            try:
                params = {**BASE_PARAMS, "api_key": TMDB_API_KEY, "page": p}
                if with_genres:
                    params["with_genres"] = with_genres

                r = requests.get(url, params=params, timeout=5)
                r.raise_for_status()

                for m in r.json().get("results", []):
                    mid = m.get("id")
                    if not mid or mid in seen_ids:
                        continue
                    seen_ids.add(mid)
                    pool.append(m)

            except requests.exceptions.RequestException as e:
                # 途中のページが失敗しても、取得済みのデータで続行する
                logger.warning(f"[TMDB_PAGE_ERROR] Page {p} fetch failed. Reason: {e}")
                continue

        # 5. 取得結果のチェック
        if not pool:
            logger.info(f"[TMDB_NO_RESULTS] No movies found for genres: {with_genres}")
            return []

        # 6. ランダムに5件抽出
        k = min(5, len(pool))
        items = random.sample(pool, k=k)

        # 7. データの整形
        formatted = []
        for m in items:
            ids = m.get("genre_ids", [])
            names = [gmap.get(i) for i in ids if gmap.get(i)]
            formatted.append({
                "id": m.get("id"),
                "title": m.get("title"),
                "overview": TmdbMovieService.truncate_text(m.get("overview"), 80),
                "poster_url": (
                    f"https://image.tmdb.org/t/p/w342{m['poster_path']}"
                    if m.get("poster_path") else None
                ),
                "genres": names,
                "rating": round(float(m.get("vote_average", 0)) / 2, 1)
            })
            
        logger.info(f"[TMDB_SUCCESS] Formatted {len(formatted)} movies successfully.")
        return formatted
    
    # 映画作品検索機能 
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
            data = response.json()
            logger.info(f"[TMDB_SEARCH] Query: {query}, Found: {len(data.get('results', []))}")
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"[TMDB_SEARCH_ERROR] Query: {query}, Error: {e}")
            return []

    # 映画作品詳細表示
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
            logger.error(f"[TMDB_DETAIL_ERROR] ID: {movie_id}, Error: {e}")
            return None
        
    # 映画作品監督表示
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
            logger.error(f"[TMDB_DIRECTOR_ERROR] ID: {movie_id}, Error: {e}")
            return None

    # 映画記録作成 (「詳細情報」+「監督名」をテンプレート表示できるように整形)
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