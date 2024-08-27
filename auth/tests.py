from jwt.exceptions import DecodeError
from rest_framework.test import APITestCase
from rest_framework import status

from auth.models import User
from auth.services.jwt import ConfirmationToken


class AuthTest(APITestCase):

    def test_register_user(self):
        data = {"email": "testuser@mail.ru", "password": "testpassword1"}
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_weak_password(self):
        data = {"email": "testuser@mail.ru", "password": "testpassword"}
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        User.objects.create_user(
            username="testuser1",
            email="testuser@mail.ru",
            password="testpassword1",
            is_active=True,
        )
        data = {"email": "testuser@mail.ru", "password": "testpassword1"}
        response = self.client.post("/auth/login", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_not_found(self):
        data = {"email": "testuser@mail.ru", "password": "testpassword1"}
        response = self.client.post("/auth/login", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ResetPasswordTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="testuser@mail.ru", password="testpassword", username="testuser"
        )
        self.client.force_authenticate(user=self.user)

    def test_reset_password(self):
        data = {"new_password": "testpassword2"}
        response = self.client.post("/auth/reset_password", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_weak_password(self):
        data = {"new_password": "testpassword"}
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ConfirmAccountTest(APITestCase):

    def test_confirm_account(self):
        User.objects.create(
            email="testuser@mail.ru", password="testpassword1", is_active=True
        )
        token = ConfirmationToken().encode(email="testuser@mail.ru")
        response = self.client.get(f"/auth/confirm_account/{token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_account_wrong_token(self):
        User.objects.create(
            email="testuser@mail.ru", password="testpassword1", is_active=True
        )

        with self.assertRaises(DecodeError):
            self.client.get(f"/auth/confirm_account/invalid_token")

    def test_confirm_account_user_not_found(self):
        token = ConfirmationToken().encode(email="testuser@mail.ru")
        response = self.client.get(f"/auth/confirm_account/{token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
