import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


class UserRegistrationTestCase(APITestCase):
    url = reverse("user:register")
    url_login = reverse("user:token_obtain_pair")

    def test_user_registration(self):
        data = {
            "email": "selamet@mail.com",
            "password": "qwe123123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_unique_name(self):
        self.test_user_registration()
        data = {
            "email": "selamet@mail.com",
            "password": "qwe123123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)


class UserLoginTestCase(APITestCase):
    url_login = reverse("user:token_obtain_pair")

    def setUp(self):
        self.username = 'selamet@mail.com'
        self.password = "qwe123123"
        self.user = User.objects.create_user(username=self.username, email=self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login, {'username': 'selamet@mail.com', 'password': 'qwe123123'})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(self.url_login, {'username': 'selamet_hatali@mail.com', 'password': 'qwe123123'})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {'username': '', 'password': ''})
        self.assertEqual(400, response.status_code)

