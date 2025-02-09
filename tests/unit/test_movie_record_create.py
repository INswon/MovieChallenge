from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
from PIL import Image
import io


class MovieRecordCreateTestCase(TestCase):
    #映画記録の作成機能 (Create) に関するテストケース
    
    def setUp(self):
        #テスト用のユーザーを作成し、ログインする
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_movie_record_valid_data(self):
        #【テスト内容】正しいデータを使って映画記録を作成できることを確認
        #【期待する動作】正常に作成され、リダイレクトされる
        
        # 1x1ピクセルのダミー画像を作成
        image = Image.new('RGB', (1, 1), color='white')
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)

        poster_file = ContentFile(img_io.getvalue(), name='new_movie_poster.png')

        # 映画データを作成
        data = {
            'title': 'New Movie',
            'poster': poster_file,  # ダミー画像を渡す
            'date_watched': timezone.now().date(),  # 適切な日付
            'rating': 5
        }

        response = self.client.post(reverse('movies:create'), data)

        # 302リダイレクトを確認（正常作成時の動作）
        self.assertEqual(response.status_code, 302)
        # DBにレコードが正しく作成されているか確認
        self.assertTrue(UserMovieRecord.objects.filter(title='New Movie').exists())

    def test_create_movie_record_invalid_data(self):
        
        #【テスト内容】無効なデータを送信した場合、バリデーションエラーが発生することを確認
        #【期待する動作】エラーメッセージが適切に表示される
    
        invalid_cases = [
            {'title': '', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 5},  # タイトルとポスターが空
            {'title': 'New Movie', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 0},  # 無効な評価
            {'title': 'New Movie', 'poster': ContentFile(b'', name=''), 'date_watched': '2024-10-03', 'rating': 'five'},  # 評価が文字列
        ]

        for data in invalid_cases:
            response = self.client.post(reverse('movies:create'), data)

            # バリデーションエラーが発生していることを確認
            form = response.context['form']
            self.assertTrue(form.errors)

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
        
        #【テスト内容】新規ユーザー登録が成功するか確認
        #【期待する動作】正常に登録され、リダイレクトされる
    
        response = self.client.post(reverse('users:signup'), {
            'username': 'testregister',
            'password1': 'registerpassword',
            'password2': 'registerpassword',
        })

        # ステータスコード 302（リダイレクト）を確認
        self.assertEqual(response.status_code, 302)
        # DBにユーザーが作成されたことを確認
        self.assertTrue(User.objects.filter(username='testregister').exists())

    def test_user_login_success(self):
        
        #【テスト内容】正しい資格情報でのログインが成功するか確認
        #【期待する動作】ログイン成功後、リダイレクトされる
        
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_movie_record_create(self):
        
        #【テスト内容】サンプルデータで映画記録を作成できるか確認
        #【期待する動作】正常に作成され、リダイレクトされる
        
        image = Image.new('RGB', (1, 1), color='white')
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)

        poster_file = ContentFile(img_io.getvalue(), name='sample_movie_poster.jpg')

        data = {
            'title': 'Sample Movie',
            'poster': poster_file,
            'date_watched': timezone.now().date(),
            'rating': 5,
        }

        response = self.client.post(reverse('movies:create'), data)

        # ステータスコードを確認（302: 成功時のリダイレクト）
        self.assertEqual(response.status_code, 302)
        # DBにレコードが作成されていることを確認
        self.assertTrue(UserMovieRecord.objects.filter(title='Sample Movie').exists())

    def test_404_error_handling(self):
        
        #【テスト内容】存在しないURLにアクセスした場合、404エラーページが表示されるか確認
        #【期待する動作】ステータスコード404、適切なテンプレートが使用される
        
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'test_templates/404.html')
