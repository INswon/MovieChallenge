from django.test import TestCase, Client
from django.urls import reverse

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profile_view_uses_correct_template(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
