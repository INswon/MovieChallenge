# 1: 2,3のコマンドが失敗した場合即時終了
set -e

# 2: Database migration 設定
echo "===== ENTRYPOINT START ====="
echo "Run migrations"
python3 manage.py migrate --noinput || echo "!!! MIGRATE FAILED !!!"
echo "Run showmigrations"
python3 manage.py showmigrations || true

# 3:静的ファイル配信設定
echo "Collect static files"
python3 manage.py collectstatic --noinput

# 4: Application startup 設定
echo "Start gunicorn"
exec python3 -m gunicorn MovieChallenge.wsgi:application --bind 0.0.0.0:8000