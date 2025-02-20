from django.test import TestCase
from django.urls import reverse
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from movies.models import UserMovieRecord
from django.utils import timezone
from PIL import Image
import io

#JPEG画像テストデータ作成
def create_dummy_image():
    image = Image.new("RGB", (1,1), color="white")
    img_io = io.BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name="test_poster.jpg")

class MovieCreateToListIntegrationTest(TestCase):

    #事前準備: ユーザー作成 & ログイン
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    #映画記録を作成後、リダイレクトされるか確認
    def test_create_movie_and_redirect(self):
        
        self.client.login(username='testuser', password='testpass') 

        poster_file = create_dummy_image()

        response = self.client.post(reverse('movies:create'), {
            'title': 'Test Movie',
            'poster': poster_file,
            'rating': '5',
            'date_watched': timezone.now().date(),
        })

        self.assertEqual(response.status_code, 302)  

    #映画記録を作成後、一覧ページに表示されるか確認
    def test_create_movie_and_check_list(self):
        
        self.client.login(username='testuser', password='testpass')  

        poster_file = create_dummy_image()

        # 映画を作成
        self.client.post(reverse('movies:create'), {
            'title': 'Test Movie',
            'poster': poster_file,
            'rating': 5,
            'date_watched': timezone.now().date(),
        })
        response = self.client.get(reverse('movies:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    #未ログインユーザーは映画を作成できず、ログインページにリダイレクトされるか確認
    def test_unauthenticated_user_cannot_create_movie(self):
    
        self.client.logout()  

        poster_file = create_dummy_image()
        response = self.client.post(reverse('movies:create'), {
            'title': 'Unauthorized Movie',
            "poster": poster_file, 
            'rating': 3,
            'date_watched': timezone.now().date(),
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    #最大文字２０文字以内なら正常に登録できる
    def test_create_movie_title_max_length(self):
        self.client.login(username = "testuser", password="testpass")
        max_length_title = "A" * 20
        poster_file = create_dummy_image()
        response = self.client.post(reverse("movies:create"),{
            "title": max_length_title,
            "poster": poster_file, 
            "rating": 5,
            "date_watched": timezone.now().date(),
        })
        self.assertEqual(response.status_code, 302)
