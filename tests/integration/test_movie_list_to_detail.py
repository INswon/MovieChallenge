from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import io

# JPEG画像テストデータ作成
def create_dummy_image():
    image = Image.new("RGB", (1,1), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name="test_poster.jpg")

class MovieListToDetailIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.poster_file = create_dummy_image()  
        self.fixed_date = timezone.datetime(2025, 2, 3).date()  

        # 映画記録を作成（ポスター画像あり）
        self.movie = UserMovieRecord.objects.create(
            user=self.user,
            title="Test Movie",
            poster=self.poster_file, 
            rating=5,
            date_watched=self.fixed_date,
        )

        # 他のユーザーとその映画データを作成
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.other_movie = UserMovieRecord.objects.create(
            user=self.other_user,
            title="Other User Movie",
            poster=self.poster_file, 
            rating=3,
            date_watched=self.fixed_date,
        )

        
    #ログイン済みユーザーが一覧画面にアクセスできるか(その他のログインユーザー情報は閲覧できない）ことの検証
    def test_list_page_accessible_by_logged_in_user(self):
        response = self.client.get(reverse("movies:home"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "movies/home.html")
        self.assertContains(response, "Test Movie")
        self.assertNotContains(response, "Other User Movie")


    # 映画記録が一覧画面で確認できるか検証(映画ポスターを登録したケース)
    def test_movie_with_poster_image_is_displayed_on_list_page(self):
        
        movie_with_poster = UserMovieRecord.objects.create(
            user=self.user,
            title="Test Movie Poster",
            poster=self.poster_file,  
            rating=5,
            date_watched=self.fixed_date,
        )

        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "Test Movie Poster")
        self.assertContains(response, "5")
        formatted_date = self.fixed_date.strftime("%Y年%-m月%-d日")  
        self.assertContains(response, f"鑑賞日: {formatted_date}")
        self.assertContains(response, f' src="/media/{movie_with_poster.poster.name}"')

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

     
    #一覧ページに編集ページへのリンクがあるか検証
    def test_create_button_redirects_to_edit_page(self):
        response = self.client.get(reverse("movies:home"))

        # 一覧ページへのアクセス確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/home.html")

        edit_url = reverse("movies:edit", args=[self.movie.id])

        # ボタンタグ内の onclick 属性を確認
        self.assertContains(response, f"location.href='/movies/edit/{self.movie.id}/'")

        # 正しいページへの遷移を確認
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_record_edit.html')



    # 一覧ページに詳細ページへのリンクがあるか検証
    def test_detail_button_redirects_to_detail_page(self):
        response = self.client.get(reverse('movies:home'))

        # 一覧ページへのアクセス確認
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies/home.html")

        # 詳細ページのURLを動的に生成
        detail_url = reverse('movies:detail', args=[self.movie.id])

        # ボタンタグ内の onclick 属性を確認
        self.assertContains(response,f"location.href='/movies/detail/{self.movie.id}/")

        # 正しいページへの遷移を確認
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_record_detail.html')


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
