# 1: 2,3のコマンドが失敗した場合即時終了
set -e

# 2: Database migration 設定
echo "Run migrations"
python3 manage.py migrate --noinput

# 3: Application startup 設定
echo "Start gunicorn"
python3 -m gunicorn MovieChallenge.wsgi:application --bind 0.0.0.0:8000
