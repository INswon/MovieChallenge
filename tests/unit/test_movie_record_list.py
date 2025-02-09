from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
from django.conf import settings
import datetime

#一覧画面のテストケース作成
class UserMovieListViewTest(TestCase):

    def setUp(self):
        #　ユーザーとデータのセットアップ
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.movie1 = UserMovieRecord.objects.create(
            user = self.user,
            title = 'Movie 1', 
            poster = 'media/posters/test_movie_poster.jpg', 
            date_watched = timezone.now(),
            rating = 5
        )

        self.movie2 = UserMovieRecord.objects.create(
            user = self.user,
            title = 'Movie 2',
            poster = 'media/posters/test_movie_poster2.jpg',  
            date_watched = datetime.datetime(2024, 1, 2, tzinfo=datetime.timezone.utc),
            rating = 4
        )


    def test_logged_in_user_can_access(self):
        # ユーザー登録しているユーザーがhomeページにアクセスできるか確認
        self.client.login(username = 'testuser', password = 'testpass')
        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/home.html')


    def test_redirect_for_unauthenticated_user(self):
        response = self.client.get(reverse('movies:home'))
        expected_url = f"{settings.LOGIN_URL}?next={reverse('movies:home')}"  
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_login_with_invalid_credentials(self):
        # homeページに誤ったユーザー名とパスワードでアクセスした場合
        response = self.client.post(reverse('users:login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

        self.assertContains(response,  "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。")


    def test_context_data(self):
        # コンテキストに含まれているデータが正しいか確認
        self.client.login(username = 'testuser', password = 'testpass')
        response = self.client.get(reverse('movies:home'))
        
        # コンテキスト内の'records'に正しいデータが含まれていることを確認
        self.assertIn('records', response.context)
        records = response.context['records']
        self.assertEqual(len(records), 2) 
        self.assertEqual(records[0], self.movie1)
        self.assertEqual(records[1], self.movie2)
