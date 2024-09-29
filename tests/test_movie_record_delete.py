from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
import datetime

class MovieRecordDeleteTestCase(TestCase):

    def setUp(self):
        #　ユーザーとデータのセットアップ
        self.user = User.objects.create_user(username='testuser', password='testpass')
         # ユーザーをログイン
        self.client.login(username='testuser', password='testpass')

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

    def test_movie_record_delete(self):
        # 削除リクエストの送信
        url = reverse('delete', args=[self.movie1.id])
        response = self.client.post(url)

        #リダイレクトの確認
        self.assertRedirects(response, reverse('users:home'))
    
        # オブジェクトがデータベースから削除されたことを確認
        with self.assertRaises(UserMovieRecord.DoesNotExist):
            UserMovieRecord.objects.get(id=self.movie1.id)

    def test_delete_unauthenticated_user(self):
        # ログアウト
        self.client.logout()

        # 削除リクエストの送信
        url = reverse('delete', args=[self.movie1.id])
        response = self.client.post(url)

        # ログインページへのリダイレクトを確認
        self.assertRedirects(response, reverse('users:login'))


    
