from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone

class MovieCreateToListIntegrationTest(TestCase):

    #事前準備: ユーザー作成 & ログイン
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    #映画記録を作成後、リダイレクトされるか確認
    def test_create_movie_and_redirect(self):
        
        self.client.login(username='testuser', password='testpass') 

        response = self.client.post(reverse('movies:create'), {
            'title': 'Test Movie',
            'rating': 5,
            'date_watched': timezone.now().date(),
        })

        self.assertEqual(response.status_code, 302)  

    #映画記録を作成後、一覧ページに表示されるか確認
    def test_create_movie_and_check_list(self):
        
        self.client.login(username='testuser', password='testpass')  

        # 映画を作成
        self.client.post(reverse('movies:create'), {
            'title': 'Test Movie',
            'rating': 5,
            'date_watched': timezone.now().date(),
        })

        print("📌 DB内の映画データ:", UserMovieRecord.objects.all())  

        response = self.client.get(reverse('movies:home'))

        print("📌 レスポンスのHTML:", response.content.decode())

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Test Movie')


    #未ログインユーザーは映画を作成できず、ログインページにリダイレクトされるか確認
    def test_unauthenticated_user_cannot_create_movie(self):
    
        self.client.logout()  

        response = self.client.post(reverse('movies:create'), {
            'title': 'Unauthorized Movie',
            'rating': 3,
            'date_watched': timezone.now().date(),
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

