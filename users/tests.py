from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class LoginTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "secret123"
        User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()

    def test_login_returns_token(self):
        url = "/auth/login/"
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
