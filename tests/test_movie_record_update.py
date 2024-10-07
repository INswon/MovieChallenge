from django.test import TestCase
from django.urls import reverse
from django.core.files.base import ContentFile
from django.utils import timezone
from movies.models import UserMovieRecord
from django.contrib.auth.models import User


class UpdateMovieRecordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        # 初期データを作成
        self.record = UserMovieRecord.objects.create(
            title='Original Title',
            poster='path/to/original_poster.png',
            date_watched=timezone.now().date(),
            rating=3,
            user=self.user
        )

    def check_form_error(self, data, field_name, expected_error):
        response = self.client.post(reverse('movies:movie_edit', args=[self.record.id]), data)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn(expected_error, form.errors[field_name])

    def test_update_movie_record_success(self):
        data = {
            'title': 'Updated Title',
            'poster': 'path/to/new/poster.jpg',
            'rating': 5,
            'date_watched': '2024-10-07',
        }
        response = self.client.post(reverse('movies:movie_edit', args=[self.record.id]), data)
        self.assertEqual(response.status_code, 302)
        self.record.refresh_from_db()
        self.assertEqual(self.record.title, 'Updated Title')
        self.assertEqual(self.record.rating, 5)

    def test_update_movie_record_title_empty(self):
        data = {
            'title': '',
            'poster': ContentFile(b'some_data', name='poster.jpg'),  # 有効な画像データに変更
            'date_watched': timezone.now().date(),
            'rating': 4,
        }
        self.check_form_error(data, 'title', 'このフィールドは必須です。')

    def test_update_movie_record_invalid_date(self):
        data = {
            'title': 'Updated Title',
            'poster': ContentFile(b'some_data', name='poster.jpg'),  # 有効な画像データに変更
            'date_watched': 'invalid-date',
            'rating': 4,
        }
        self.check_form_error(data, 'date_watched', '日付を正しく入力してください。')

    def test_update_movie_record_invalid_rating(self):
        data = {
            'title': 'Updated Title',
            'poster': ContentFile(b'some_data', name='poster.jpg'),  # 有効な画像データに変更
            'date_watched': timezone.now().date(),
            'rating': 0,
        }
        self.check_form_error(data, 'rating', '評価は1から5の間で選択してください。')

    def test_update_nonexistent_movie_record(self):
        response = self.client.post(reverse('movies:movie_edit', args=[9999]), {
            'title': 'Updated Title',
            'poster': ContentFile(b'some_data', name='poster.jpg'),  # 有効な画像データに変更
            'date_watched': timezone.now().date(),
            'rating': 4,
        })
        self.assertEqual(response.status_code, 404)

    def test_update_movie_record_unauthenticated(self):
        self.client.logout()
        data = {
            'title': 'Updated Title',
            'poster': 'path/to/new/poster.jpg',
            'rating': 5,
            'date_watched': '2024-10-07',
        }
        response = self.client.post(reverse('movies:movie_edit', args=[self.record.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)
