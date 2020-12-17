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
