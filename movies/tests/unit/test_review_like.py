from django.test import TestCase
from movies.models import UserMovieRecord,Review,Like,Genre
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class RevieLikeTest(TestCase):
    
    def setUp(self):
        # ユーザーを2人用意（投稿者とレビューする人）
        self.userA = User.objects.create_user(username="userA", password="pass") #映画鑑賞投稿者
        self.userB = User.objects.create_user(username="userB", password="pass") #レビュー投稿者

        # ジャンルを複数作成（汎用的なジャンル名を使用）
        genre_action = Genre.objects.create(name="アクション")
        genre_sci_fi = Genre.objects.create(name="SF")
        
        # ユーザーAが映画記録を投稿(TmdbAPIから取得したことを前提に作成)
        self.movie = UserMovieRecord.objects.create(
            user=self.userA,
            title="テスト映画タイトル",
            date_watched=timezone.now().date(),
            poster_url="https://example.com/test-poster.jpg",  
            tmdb_id=1111,  # 任意のID（API用の再取得確認などに使われる）
            director="テスト監督名",
            comment="これはテスト用の映画感想です。",
            rating=4 
        )

        # ジャンルをM2Mで追加（1つ以上あればOK）
        self.movie.genres.add(genre_action, genre_sci_fi)

        # ユーザーBがレビューを投稿
        self.review = Review.objects.create(
            user=self.userB,
            movie=self.movie,
            content="テストレビュー"
        )
        

    def test_like_post_creates_like(self):
        self.client.force_login(self.userA)

        # AjaxでPOSTリクエストを送る
        response = self.client.post(
            f"/movies/review_like/{self.review.id}/",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        # レスポンス内容とLikeの作成を検証
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["liked"])
        self.assertEqual(Like.objects.filter(user=self.userA, review=self.review).count(), 1)


    def test_like_deleted_when_already_liked(self):
        self.client.force_login(self.userA)

        # いいね済みの状態を作る
        Like.objects.create(user=self.userA, review=self.review, movie=self.movie)

        # Ajaxで再度POST（トグルでOFF状態にする）
        response = self.client.post(
            f"/movies/review_like/{self.review.id}/",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        # ステータス200・liked: false を確認
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["liked"])

        # DBからLikeが削除されたことを確認
        self.assertEqual(Like.objects.filter(user=self.userA, review=self.review).count(), 0)



    
