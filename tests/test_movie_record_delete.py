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

        # 別のユーザーとその映画記録の作成
        self.another_user = User.objects.create_user(username='anotheruser', password='anotherpass')

        self.another_movie = UserMovieRecord.objects.create(
            user=self.another_user,
            title='Another Movie',
            poster='media/posters/another_movie_poster.jpg',
            date_watched=timezone.now(),
            rating=3
        )


    def test_movie_record_delete(self):
        # 削除リクエストの送信
        url = reverse('movies:delete', args=[self.movie1.id])
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
        url = reverse('movies:delete', args=[self.movie1.id])
        response = self.client.post(url)

        # ログインページへのリダイレクトを確認
        self.assertRedirects(response, f"{reverse('users:login')}?next={url}")


    def test_delete_nonexistent_record(self):
        # 存在しないIDで削除リクエストの送信
        url = reverse('movies:delete', args=[999])  
        response = self.client.delete(url)

        # 404エラーページが表示されることを確認
        self.assertEqual(response.status_code, 404)


    
    def test_delete_another_user_record(self):
        # 別のユーザーとしてログイン
        self.client.logout()
        self.client.login(username='anotheruser', password='anotherpass')

        # 他のユーザーの映画記録を削除しようとする
        url = reverse('movies:delete', args=[self.movie1.id])
        response = self.client.delete(url)

        # アクセス拒否エラーページが表示されることを確認
        self.assertEqual(response.status_code, 403) 
