from rest_framework.test import APITestCase
from auth.models import User
from feed.models import Ad, Comment


class AdModelViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@mail.ru", password="testpassword", username="testuser"
        )
        self.client.force_authenticate(user=self.user)
        self.admin = User.objects.create_user(
            email="testuser2@mail.ru",
            password="testpassword2",
            username="testuser2",
            role="AD",
        )

    def test_create_ad(self):
        data = {"title": "Test Ad", "price": 150}
        response = self.client.post("/feed/ad", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_ad_missing_data(self):
        response = self.client.post("/feed/ad", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_ad(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        data = {"title": "Updated Ad", "price": 180}
        response = self.client.patch(f"/feed/ad/{ad.id}", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_update_ad_not_owner(self):
        self.client.force_authenticate(user=self.user)
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.admin)
        data = {"title": "Updated Ad"}
        response = self.client.patch(f"/feed/ad/{ad.id}", data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_update_ad_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        data = {"title": "Updated Ad"}
        response = self.client.patch(f"/feed/ad/{ad.id}", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_ad_list(self):
        response = self.client.get("/feed/ad")
        self.assertEqual(response.status_code, 200)

    def test_get_ad_detail(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        response = self.client.get(f"/feed/ad/{ad.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_ad(self):
        response = self.client.get("/feed/ad/999")
        self.assertEqual(response.status_code, 404)


class CommentModelViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.admin = User.objects.create_user(
            email="testuser2@mail.ru",
            password="testpassword2",
            username="testuser2",
            role="AD",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        data = {"text": "Test comment", "ad_id": ad.id}
        response = self.client.post(f"/feed/{ad.id}/comment", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_comment_missing_data(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        response = self.client.post(f"/feed/{ad.id}/comment", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_comment(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        comment = Comment.objects.create(text="Test comment", author=self.user, ad=ad)
        data = {"text": "Updated comment"}
        response = self.client.patch(
            f"/feed/{ad.id}/comment/{comment.id}", data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_comment_not_owner(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        comment = Comment.objects.create(text="Test comment", author=self.admin, ad=ad)
        data = {"text": "Updated comment"}
        response = self.client.patch(
            f"/feed/{ad.id}/comment/{comment.id}", data, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_update_comment_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        comment = Comment.objects.create(text="Test comment", author=self.user, ad=ad)
        data = {"text": "Updated comment"}
        response = self.client.patch(
            f"/feed/{ad.id}/comment/{comment.id}", data, format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_comment_invalid_data(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        comment = Comment.objects.create(text="Test comment", author=self.user, ad=ad)
        data = {"invalid_field": "Updated comment"}
        response = self.client.patch(
            f"/feed/{ad.id}/comment/{comment.id}", data, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_get_comment_list(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        response = self.client.get(f"/feed/{ad.id}/comment")
        self.assertEqual(response.status_code, 200)

    def test_get_comment_detail(self):
        ad = Ad.objects.create(title="Test Ad", price=150, author=self.user)
        comment = Comment.objects.create(text="Test comment", author=self.user, ad=ad)
        response = self.client.get(f"/feed/{ad.id}/comment/{comment.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_comment(self):
        response = self.client.get("/feed/999/comment/999")
        self.assertEqual(response.status_code, 404)
