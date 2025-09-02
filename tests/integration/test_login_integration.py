from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class UserLoginIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username = "testuser", password = "testpass")

    #正しい情報でログインできるか検証
    def test_login_success(self):
        response = self.client.post(reverse("users:login"), {
            "username": "testuser",  
            "password": "testpass"
        })
        self.assertRedirects(response, reverse("movies:home"))

    #誤った情報を入力した際ログイン失敗することの検証(username)
    def test_login_fail_nonexistent_user(self):
        response = self.client.post(reverse("users:login"), {
            "username": "wronguser",  
            "password": "testpass"  
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "正しいユーザー名とパスワードを入力してください") 

    #誤った情報を入力した際ログイン失敗することの検証(password)
    def test_login_fail_nonexistent_password(self):
        response = self.client.post(reverse("users:login"), {
            "username": "testuser",  
            "password": "wrongpass"  
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "正しいユーザー名とパスワードを入力してください") 

    #空の入力でログイン失敗することの検証
    def test_login_fail_empty_fields(self):
        response = self.client.post(reverse("users:login"), {
            "username": "",
            "password": ""
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "このフィールドは必須です")  

    #ログイン後のリダイレクトが正常であるか検証
    def test_login_redirects_correctly(self):
        response = self.client.post(reverse("users:login"), {
            'username': "testuser",
            'password': "testpass"
        })
        self.assertRedirects(response, reverse("movies:home")) 

    #未ログイン時、映画鑑賞一覧画面にアクセスしたらログインページにリダイレクトされることの検証
    def test_redirect_if_not_logged_in(self):
        response = self.client.get("movies:home")
        self.assertRedirects(response, reverse("users:login") + "?next=" + reverse("movies:home"))



