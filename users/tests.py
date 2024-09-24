from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone


#一覧画面のテストケース作成
class UserMovieListViewTest(TestCase):

    def setUp(self):
        #ユーザーとデータのセットアップ
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.movie1 = UserMovieRecord.objects.create(
            user=self.user,
            title='Movie 1', 
            poster='posters/test_movie_poster.jpg', 
            date_watched=timezone.now(),
            rating=5
        )

        self.movie2 = UserMovieRecord.objects.create(
            title='Movie Title 2',
            poster='path/to/poster2.jpg',
            date_watched='2024-01-02',
            rating=4
        )
    
    def test_redirect_if_not_logged_in(self):
         # ログインしていない場合は、/login/にリダイレクトされる
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/home/')  

    def test_logged_in_user_can_access(self):
        # ログインしているユーザーがリストビューにアクセスできるか
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_context_data(self):
        # コンテキストに含まれているデータが正しいか確認
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        
        # コンテキスト内の'records'に正しいデータが含まれていることを確認
        self.assertIn('records', response.context)
        records = response.context['records']
        self.assertEqual(len(records), 2)  # 登録された映画が2つ
        self.assertEqual(records[0], self.movie1)
        self.assertEqual(records[1], self.movie2)
