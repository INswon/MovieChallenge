from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
from PIL import Image
import io

class MovieRecordCreateTestCase(TestCase):

    def setUp(self):
        # ユーザーのセットアップ
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_movie_record_valid_data(self):
        # 1x1ピクセルのダミーPNG画像をPILを使って生成
        image = Image.new('RGB', (1, 1), color='white')
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)  # ポインタを最初に戻す
        
        poster_file = ContentFile(img_io.getvalue(), name='new_movie_poster.png')
        
        # 現在の日付を適切な形式で渡す
        data = {
            'title': 'New Movie',
            'poster': poster_file,  # ダミー画像を直接渡す
            'date_watched': timezone.now().date(),  # 日付を適切に渡す（DateField用）
            'rating': 5
        }

        # 映画記録を作成
        response = self.client.post(reverse('movies:create'), data)

        # 成功の確認
        self.assertEqual(response.status_code, 302)  # リダイレクトを確認
        self.assertTrue(UserMovieRecord.objects.filter(title='New Movie').exists())  # データベースにレコードが存在するか確認


    def test_create_movie_record_invalid_data(self):
        invalid_cases = [
            {'title': '', 'poster': '', 'date_watched': '2024-10-03', 'rating': 5},  # titleとposterが空
            {'title': 'New Movie', 'poster': '', 'date_watched': '2024-10-03', 'rating': 0},  # posterが空、ratingが無効
            {'title': 'New Movie', 'poster': '', 'date_watched': '2024-10-03', 'rating': 'five'},  # posterが空、ratingが文字列
        ]

        for data in invalid_cases:
            response = self.client.post(reverse('movies:create'), data)

            form = response.context['form']  # フォームを取得
            self.assertTrue(form.errors)  # フォームにエラーが存在するか確認

            # エラーメッセージの確認
            if 'title' in form.errors:
                self.assertIn('このフィールドは必須です。', form.errors['title'])
            if 'poster' in form.errors:
                self.assertIn('このフィールドは必須です。', form.errors['poster'])
            if 'rating' in form.errors:
                if data['rating'] == 0:
                    self.assertIn('評価は1から5の間で選択してください。', form.errors['rating'])
                if data['rating'] == 'five':
                    self.assertIn('整数を入力してください。', form.errors['rating'])
