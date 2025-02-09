from django.test import TestCase
from django.urls import reverse

class YourViewTests(TestCase):
    def test_existing_url_view(self):
        response = self.client.get(reverse('existing_url'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data here')  # 渡したデータが表示されることを確認