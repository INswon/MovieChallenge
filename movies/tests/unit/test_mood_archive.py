import re
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import quote
from django.shortcuts import resolve_url
from datetime import date
from movies.models import Mood, UserMovieRecord

# 映画記録データの作成
def create_record(user, mood, n=1):
    for _ in range(n):
        r = UserMovieRecord.objects.create(
            user=user,
            title="t",
            director="d",
            rating=3,
            comment="c",
            date_watched=date.today(),
            poster_url=None,
        )
        r.mood.add(mood)


class MoodPageTestCase(TestCase):
    # テスト作成データ
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.mood1 = Mood.objects.create(name="癒された")  
        self.mood2 = Mood.objects.create(name="泣いた")
        self.mood3 = Mood.objects.create(name="興奮")
        self.mood4 = Mood.objects.create(name="怖い")
        self.mood5 = Mood.objects.create(name="驚いた")

    #カテゴリー [1] 認可 / 存在性（URLを叩いたときの基本反応）
    # 感情名「癒された」でアクセスした場合、200が返る
    def test_mood_page_returns_200(self):
        create_record(self.user, self.mood1, n=1)
        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    # 存在しない感情名でアクセスした場合、404が返る
    def test_mood_page_returns_404_for_invalid_id(self):
        url = reverse("movies:mood_archive", kwargs={"mood_name": "存在しない感情"})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    # 存在する感情名だが、記録としては登録されていないデータの呼び出した時の検証
    def test_known_mood_returns_200_even_if_zero(self):
        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    # 未ログインで、感情アーカイブページに飛ぶと(/login/?next)に302でリダイレクトされる検証
    def test_requires_login_redirects_to_login(self):
        # 未ログイン状態
        self.client.logout()
        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(url)

        login_url = resolve_url(settings.LOGIN_URL)
        expected = f"{login_url}?next={quote(url)}"
        self.assertRedirects(res, expected_url=expected, status_code=302, target_status_code=200)

    #カテゴリー [2] 感情リンクボタン上位4件に該当する検証 (アーカイブ側)
    # TOP4以内の感情に対応するボタン表示の検証
    def test_top4_button_link_present_when_current_mood_is_in_top4(self):
        create_record(self.user, self.mood1, n=5)
        create_record(self.user, self.mood2, n=10)
        create_record(self.user, self.mood3, n=9)
        create_record(self.user, self.mood4, n=8)
        create_record(self.user, self.mood5, n=1)

        page_url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(page_url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f'href="{page_url}"')
        self.assertContains(res, f'{self.mood1.name}（5回）')

    # 上位4件外なら、対象ムードのリンクはTop4ボタン群に存在しない (「癒された」を5位以下に落とす)
    def test_top4_button_link_absent_when_current_mood_is_not_in_top4(self):
        create_record(self.user, self.mood1, n=2)   
        create_record(self.user, self.mood2, n=10)
        create_record(self.user, self.mood3, n=9)
        create_record(self.user, self.mood4, n=8)
        create_record(self.user, self.mood5, n=7)

        page_url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(page_url)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, f'href="{page_url}"')
    
    # 感情Top4ボタンが5件以上あっても4件に制限されることの確認
    def test_top4_shows_exactly_four_buttons_on_mood_archive(self):
        create_record(self.user, self.mood1, n=5)
        create_record(self.user, self.mood2, n=10)
        create_record(self.user, self.mood3, n=9)
        create_record(self.user, self.mood4, n=8)
        create_record(self.user, self.mood5, n=1)

        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()

        buttons = re.findall(r'class="btn mood-btn mood-[^"]+"', html)
        self.assertEqual(len(buttons), 4)

        m5 = reverse("movies:mood_archive", kwargs={"mood_name": self.mood5.name})
        self.assertNotContains(res, f'href="{m5}"')

    # 感情Top4ボタンが頻度降順で並ぶことの確認
    def test_top4_order_is_desc_by_frequency_on_mood_archive(self):
        create_record(self.user, self.mood1, n=10)
        create_record(self.user, self.mood2, n=9)
        create_record(self.user, self.mood3, n=8)
        create_record(self.user, self.mood4, n=7)

        url = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()

        urls = [reverse("movies:mood_archive", kwargs={"mood_name": m.name})
                for m in [self.mood1, self.mood2, self.mood3, self.mood4]]
        idx = [html.index(u) for u in urls]
        self.assertEqual(idx, sorted(idx))


    # 映画記録が0件のとき、ホーム画面で感情Top4ボタンが表示されないことの確認
    def test_top4_hidden_when_no_records_on_home_page(self):
        url = reverse("movies:home")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        self.assertContains(res, "まだ感情タグが登録されていません")
        self.assertNotContains(res, 'class="btn mood-btn mood-')

        m1 = reverse("movies:mood_archive", kwargs={"mood_name": self.mood1.name})
        self.assertNotContains(res, f'href="{m1}"')

    # 感情Top4ボタンが5件以上あっても4件に制限されることの確認
    def test_top4_shows_exactly_four_buttons_on_home(self):
        create_record(self.user, self.mood1, n=5)
        create_record(self.user, self.mood2, n=10)
        create_record(self.user, self.mood3, n=9)
        create_record(self.user, self.mood4, n=8)
        create_record(self.user, self.mood5, n=1)

        url = reverse("movies:home")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        html = res.content.decode()

        buttons = re.findall(r'class="btn mood-btn mood-[^"]+"', html)
        self.assertEqual(len(buttons), 4)

        m5 = reverse("movies:mood_archive", kwargs={"mood_name": self.mood5.name})
        self.assertNotContains(res, f'href="{m5}"')
        
    # 感情Top4ボタンが頻度降順で並ぶことの確認
    def test_top4_order_is_desc_by_frequency_on_home(self):
        create_record(self.user, self.mood1, n=10)
        create_record(self.user, self.mood2, n=9)
        create_record(self.user, self.mood3, n=8)
        create_record(self.user, self.mood4, n=7)

        url = reverse("movies:home")
        res = self.client.get(url)
        html = res.content.decode()

        urls = [reverse("movies:mood_archive", kwargs={"mood_name": m.name})
                for m in [self.mood1, self.mood2, self.mood3, self.mood4]]
        idx = [html.index(u) for u in urls]
        self.assertEqual(idx, sorted(idx))