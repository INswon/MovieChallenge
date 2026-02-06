from pathlib import Path
from decouple import config
import os

DEBUG = config('DEBUG', default=True, cast=bool)
LOG_LEVEL = config('DJANGO_LOG_LEVEL', default='INFO')
DEFAULT_CHARSET = 'utf-8'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "movies.apps.MoviesConfig",
    "users",
    "missions",
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MovieChallenge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "movies.context_processors.static_version",
            ],
        },
    },
]

WSGI_APPLICATION = "MovieChallenge.wsgi.application"


# データベース設定
if DEBUG:
    # ローカル環境: SQLite3
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # 本番環境: PostgreSQL設定
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",   
            "NAME": os.environ.get("DB_NAME"),           # DB名
            "USER": os.environ.get("DB_USER"),           # ユーザー名
            "PASSWORD": os.environ.get("DB_PASSWORD"),   # パスワード
            "HOST": os.environ.get("DB_HOST"),           # エンドポイント
            "PORT": "5432",                             
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# TMDb API設定
TMDB_API_KEY = config('TMDB_API_KEY')  # .envファイルからAPIキーを取得
TMDB_ACCESS_TOKEN = config('TMDB_ACCESS_TOKEN')  # .envファイルからアクセストークンを取得


# 静的ファイル
STATIC_URL = "/static/"
STATIC_VERSION = "1.0.0"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # 開発環境時のファイルディレクトリ
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # 本番環境時のファイルディレクトリ
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# メディアファイル
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = '/movies/home/'
LOGIN_URL = '/users/login/'

# セキュリティ設定
ALLOWED_HOSTS = [
    ".awsapprunner.com",  # 1. App Runner接続許可(本番環境)
    "169.254.172.3", # App Runnerヘルスチェック用 IP
    "localhost",  # 2. ローカル環境接続許可
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = ["https://g6qqzffsxu.ap-northeast-1.awsapprunner.com"]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "production": {
            # {name} を入れることで「どのファイルのログか」を CloudWatch 上で特定しやすくする
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers":{
        "console": { 
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "production",
        },
    },
    "loggers": {
        "movies": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "missions": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # RDS関連：DB接続エラー時情報を残す
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR", 
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING", # 外部ライブラリ（urllib3など）のノイズを遮断
    },
}