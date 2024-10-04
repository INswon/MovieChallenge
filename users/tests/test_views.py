from django.test import TestCase

class Custom404ViewTests(TestCase):
    def test_custom_404_view(self):
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'test_templates/404.html')
        self.assertContains(response, 'ページが見つかりません')
