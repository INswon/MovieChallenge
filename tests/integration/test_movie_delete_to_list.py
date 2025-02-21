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

poster_file = create_dummy_image()


#削除機能と結合テスト
class MovieDeleteIntegrationTest(TestCase):
     
     #テストデータ作成
     def setUp(self):
          self.user = User.objects.create_user(username='testuser', password='testpass')
          self.another_user = User.objects.create_user(username='anotheruser', password='anotherpass')

          self.movie = UserMovieRecord.objects.create(
               user=self.user,
               title="Test Movie",
               date_watched=timezone.now().date(),
               rating=5
            )
          
          self.client.login(username='testuser', password='testpass')
         

     #削除確認画面が正しく表示されることの検証
     def test_delete_confirmation_page(self):
         response = self.client.get(reverse('movies:delete', args=[self.movie.id]))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response,"movies/movie_record_delete.html")

    
     #削除ボタン押下で削除確認画面が表示されるか検証
     def test_delete_movie_and_redirect(self):
        response = self.client.post(reverse('movies:delete', args=[self.movie.id]))
        self.assertRedirects(response, reverse('movies:home')) 


     # 削除確認画面でキャンセルボタンを押すと、削除されず元のページに戻ることの検証
     def test_cancel_delete_does_not_remove_movie(self):
         response = self.client.get(reverse('movies:delete', args=[self.movie.id]))
         self.assertEqual(response.status_code, 200)

    #データベースから実際に削除されていることの検証
     def test_movie_is_deleted_from_database(self):
         self.client.post(reverse("movies:delete", args=[self.movie.id]))
         self.assertFalse(UserMovieRecord.objects.filter(id=self.movie.id).exists())

     # 削除対象の映画鑑賞記録が存在しない場合、404エラーになることの検証
     def test_delete_nonexistent_movie_returns_404(self):
        response = self.client.post(reverse('movies:delete', args=[99999]))
        self.assertEqual(response.status_code, 404)

     #他のユーザーが映画鑑賞記録を削除できないことの検証
     def test_other_user_cannot_delete_movie(self):
        self.client.logout()
        self.client.login(username='anotheruser', password='anotherpass')

        response = self.client.post(reverse('movies:delete', args=[self.movie.id]))

        if response.status_code == 302:
            self.assertTrue(response.url.startswith(reverse('movies:home')))
        else:
            self.assertEqual(response.status_code, 403)
