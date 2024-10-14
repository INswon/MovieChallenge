from .models import MovieWatch
from django.utils import timezone
from datetime import timedelta

#ミッションの達成条件を評価するクラス。
class CriteriaEvaluator:

    def __init__(self, user, criteria):
        self.user = user
        self.criteria = criteria
        self.today = timezone.now().date()

    def evaluate(self):

        #全ての条件を評価し、全て満たしていれば True を返す。
        #各条件を順に評価

        checks = [
            self.check_min_watch_count,
            self.check_min_genres,
            self.check_min_directors,
            self.check_consecutive_months,
            self.check_min_classic,
            self.check_min_foreign,
            self.check_min_recent,
            self.check_min_watched_with_friends,
            self.check_min_movie_per_day,
        ]

        for check in checks:
            if not check():
                return False

        return True

    def check_min_watch_count(self):
        min_watch = self.criteria.get("min_watch_count")
        if min_watch is not None:
            watch_count = MovieWatch.objects.filter(user=self.user).count()
            if watch_count < min_watch:
                return False
        return True

    def check_min_genres(self):
        min_genres = self.criteria.get("min_genres")
        if min_genres is not None:
            genre_count = MovieWatch.objects.filter(user=self.user).values('movie__genre').distinct().count()
            if genre_count < min_genres:
                return False
        return True

    def check_min_directors(self):
        min_directors = self.criteria.get("min_directors")
        if min_directors is not None:
            director_count = MovieWatch.objects.filter(user=self.user).values('movie__director').distinct().count()
            if director_count < min_directors:
                return False
        return True

    def check_consecutive_months(self):
        consecutive_months = self.criteria.get("consecutive_months")
        if consecutive_months is not None:
            start_date = self.today - timedelta(days=30 * consecutive_months)
            watch_months = MovieWatch.objects.filter(
                user=self.user,
                watched_at__gte=start_date
            ).dates('watched_at', 'month').count()
            if watch_months < consecutive_months:
                return False
        return True

    def check_min_classic(self):
        min_classic = self.criteria.get("min_classic")
        if min_classic is not None:
            classic_count = MovieWatch.objects.filter(user=self.user, movie__is_classic=True).count()
            if classic_count < min_classic:
                return False
        return True

    def check_min_foreign(self):
        min_foreign = self.criteria.get("min_foreign")
        if min_foreign is not None:
            foreign_count = MovieWatch.objects.filter(user=self.user, movie__is_foreign=True).count()
            if foreign_count < min_foreign:
                return False
        return True

    def check_min_recent(self):
        min_recent = self.criteria.get("min_recent")
        if min_recent is not None:
            date_threshold = self.today - timedelta(days=365)
            recent_count = MovieWatch.objects.filter(
                user=self.user,
                movie__release_date__gte=date_threshold
            ).count()
            if recent_count < min_recent:
                return False
        return True

    def check_min_watched_with_friends(self):
        min_watched_with_friends = self.criteria.get("min_watched_with_friends")
        if min_watched_with_friends is not None:
            watched_with_friends_count = MovieWatch.objects.filter(
                user=self.user,
                watched_with_friends=True
            ).count()
            if watched_with_friends_count < min_watched_with_friends:
                return False
        return True

    def check_min_movie_per_day(self):
        min_movie_per_day = self.criteria.get("min_movie_per_day")
        if min_movie_per_day is not None:
            watch_today_count = MovieWatch.objects.filter(
                user=self.user,
                watched_at__date=self.today
            ).count()
            if watch_today_count < min_movie_per_day:
                return False
        return True
