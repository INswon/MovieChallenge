from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
from django.conf import settings 
from PIL import Image
import io
import shutil
import tempfile
import os

# JPEG画像テストデータ作成
def create_dummy_image(name="test_poster.jpg"):
    image = Image.new("RGB", (1, 1), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name=name)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())  # テスト用の一時ディレクトリを使用

class MovieEditIntegrationTest(TestCase):

    def setUp(self):
        # テスト用データ作成
        self.user = User.objects.create_user(username="testuser", password="testpass")

        initial_poster = create_dummy_image()

        self.movie = UserMovieRecord.objects.create(
            user=self.user,
            title="Original Movie",
            date_watched=timezone.now().date(),
            rating=3,
            poster=initial_poster 
        )

        self.client.login(username="testuser", password="testpass")

    def tearDown(self):
        # テスト終了時にMEDIA_ROOTの内容を削除
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    # タイトル・評価・視聴日・画像の編集が正しく更新されるか検証
    def test_edit_movie_successfully(self):
        new_poster = create_dummy_image(name="new_test_poster.jpg")
        response = self.client.post(reverse('movies:edit', args=[self.movie.id]), {
            "title": "Updated Movie",
            "poster": new_poster,
            "date_watched": "2024-02-01",
            "rating": 5
        })

        self.assertRedirects(response, reverse("movies:home"))

        # データが正しく更新されたか確認
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Updated Movie")
        self.assertEqual(self.movie.rating, 5)
        self.assertEqual(self.movie.date_watched.strftime("%Y-%m-%d"), "2024-02-01")

        # 画像が更新されたか確認
        self.assertTrue(bool(self.movie.poster))
        self.assertTrue(os.path.exists(self.movie.poster.path))
        self.assertNotEqual(self.movie.poster.name, "test_poster.jpg")  

    # 画像を変更せずにタイトルだけ編集した場合の動作を検証
    def test_edit_movie_without_changing_poster(self):
        old_poster_name = self.movie.poster.name  # 変更前の画像名を保存
        response = self.client.post(reverse('movies:edit', args=[self.movie.id]), {
            "title": "Updated Movie",
            "date_watched": "2024-02-01",
            "rating": 5
        })

        self.assertRedirects(response, reverse("movies:home"))

        # データが正しく更新されたか確認
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Updated Movie")
        self.assertEqual(self.movie.rating, 5)
        self.assertEqual(self.movie.date_watched.strftime("%Y-%m-%d"), "2024-02-01")

        # 画像は変更されていないことを確認
        self.assertEqual(self.movie.poster.name, old_poster_name)

    # 画像をクリアした場合、画像が削除されデフォルト画像が表示されるか確認
    def test_remove_poster_and_display_default_image(self):
        self.assertTrue(bool(self.movie.poster))
        old_poster_path = self.movie.poster.path

        response = self.client.post(reverse('movies:edit', args=[self.movie.id]), {
            "title": "Updated Movie",
            "date_watched": "2024-02-01",
            "rating": 5,
            "delete_poster": "on"  
        })

        self.assertRedirects(response, reverse("movies:home"))
        
        # データベースの更新を確認
        self.movie.refresh_from_db()
        self.assertFalse(bool(self.movie.poster))
        
        # 実際のファイルが削除されていることを確認
        self.assertFalse(os.path.exists(old_poster_path))

        # フロントエンドでデフォルト画像が表示されることを確認
        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)
        
        expected_img_src = 'src="/static/images/default_poster.jpg?v=1.0.0"'
        self.assertContains(response, expected_img_src, html=False)
