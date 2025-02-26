from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone

class MovieListToDetailIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # ユーザーの映画鑑賞記録を作成（固定日付を使用）
        self.fixed_date = timezone.datetime(2025, 1, 1).date()
        self.movie = UserMovieRecord.objects.create(
            user=self.user,
            title="Test Movie",
            rating=5,
            date_watched=self.fixed_date
        )

     #一覧ページに新規作成ページのリンクがあるか確認
    def test_create_button_redirects_to_create_page(self):
        response = self.client.get(reverse("movies:home"))

        # 一覧ページへのアクセス確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/home.html")
        
        create_url = reverse('movies:create')

        # ボタンタグ内の onclick 属性を確認
        self.assertContains(response, f"location.href='/movies/create/'")

        # 正しいページへの遷移を確認
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_record_create.html')


    #一覧ページに詳細ページへのリンクがあるか検証
    def test_list_page_has_detail_link(self):
        
        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)

        detail_url = reverse('movies:detail', args=[self.movie.id])
        self.assertContains(response, f'<a href="{detail_url}">')


    #一覧ページ → 詳細ページに遷移し、映画情報が正しく表示されるか検証
    def test_list_to_detail_page_shows_correct_movie_info(self):
        
        #一覧ページへアクセス
        list_response = self.client.get(reverse('movies:home'))
        self.assertEqual(list_response.status_code, 200)

        # 詳細ページのURLを取得
        detail_url = reverse('movies:detail', args=[self.movie.id])

        #詳細ページに遷移
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)

        #詳細ページに映画情報が表示されていることを確認
        self.assertContains(detail_response, "<h1>Test Movie</h1>")
        self.assertContains(detail_response, "5")  
