from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
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
            {'title': '', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 5},  # titleとposterが空
            {'title': 'New Movie', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 0},  # posterが空、ratingが無効
            {'title': 'New Movie', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 'five'},  # posterが空、ratingが文字列
        ]

        for data in invalid_cases:
            response = self.client.post(reverse('movies:create'), data)

            form = response.context['form']  # フォームを取得
            self.assertTrue(form.errors)  # フォームにエラーが存在するか確認

            # エラーメッセージの確認
            if 'title' in form.errors:
                self.assertIn('このフィールドは必須です。', form.errors['title'])
            if 'poster' in form.errors:
                self.assertIn('入力されたファイルは空です。', form.errors['poster'])
            if 'rating' in form.errors:
                if data['rating'] == 0:
                    self.assertIn('評価は1から5の間で選択してください。', form.errors['rating'])
                if data['rating'] == 'five':
                    self.assertIn('整数を入力してください。', form.errors['rating'])


    def test_user_registration(self):
        # ユーザー登録のテスト
        response = self.client.post(reverse('users:signup'), {
            'username': 'testregister',  # ユーザー名
            'password1': 'registerpassword',  # パスワード
            'password2': 'registerpassword',  # 確認用のパスワード
        })

        # ステータスコードが 200 の場合、フォームエラーが発生することの確認
        if response.status_code == 200:
            print(response.context['form'].errors) 

        # 正しく登録される場合は 302 リダイレクトが発生することの確認
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testregister').exists())


    def test_user_login_success(self):
        # 正しい資格情報でのログインテスト
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',  # setUpで作成したユーザー名
            'password': 'testpass',   # setUpで設定したパスワード
        })
        self.assertEqual(response.status_code, 302)  # ログイン後にリダイレクトされることを確認
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # ユーザーが認証されていることを確認

    def test_movie_record_create(self):
        # テスト用のデータを作成
        # 1x1ピクセルのダミーPNG画像をPILを使って生成
        image = Image.new('RGB', (1, 1), color='white')
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)  # ポインタを最初に戻す
        
        poster_file = ContentFile(img_io.getvalue(), name='sample_movie_poster.jpg')
        
        data = {
            'title': 'Sample Movie',
            'poster': poster_file,  # ダミー画像を直接渡す
            'date_watched': timezone.now().date(),  # 日付を現在時刻として渡す
            'rating': 5,
        }
        
        response = self.client.post(reverse('movies:create'), data)
        # レスポンスのステータスをチェック
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(UserMovieRecord.objects.filter(title='Sample Movie').exists())  # データベースにレコードが存在するか確認

    def test_404_error_handling(self):
        # 存在しないページへのアクセス
        response = self.client.get('/nonexistent-url/')

        # ステータスコードが404であることを確認
        self.assertEqual(response.status_code, 404)
    
        # エラーページのテンプレートが正しく表示されているか確認
        self.assertTemplateUsed(response, 'test_templates/404.html')
    
