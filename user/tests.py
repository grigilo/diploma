from rest_framework.test import APITestCase
from rest_framework import status

from auth.models import User


class UserCRUDTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="testuser@mail.ru"
        )
        self.client.force_authenticate(user=self.user)

    def test_read_me(self):
        response = self.client.get("/user/me")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "testuser@mail.ru")

    def test_update_me(self):
        data = {"first_name": "updateduser"}
        response = self.client.patch("/user/me", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "updateduser")

    def test_delete_me(self):
        response = self.client.delete("/user/me")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_read_user_profile(self):
        response = self.client.get(f"/user/profile/{self.user.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "testuser@mail.ru")
