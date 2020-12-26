import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from event.models import Event


class BaseTestCase(APITestCase):
    url = '/api/event/'
    login_url = reverse('user:token_obtain_pair')

    def setUp(self):
        self.username = 'selamet@mail.com'
        self.password = "qwe123123"
        self.user = User.objects.create_user(username=self.username, email=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.login_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


class EventCreateTestCase(BaseTestCase):

    def test_event_create(self):
        data = {
            "title": "selamet@mail.com",
            "date": "2020-11-26 19:33"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_create_invalid(self):
        data = {
            "title": "selamet@mail.com",
            "date": "12112"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

        data = {
            "title": "",
            "date": "2020-11-26 19:33"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_create_unauthorized(self):
        self.client.credentials()
        data = {
            "title": "selamet@mail.com",
            "date": "2020-11-26 19:33"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)


class GetEventTestCase(BaseTestCase):

    def test_event_create(self):
        data = {
            "title": "selamet@mail.com",
            "date": "2020-11-26 19:33"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_get_events(self):
        self.test_event_create()
        self.url += '?from=2020-11-25&to=2021-1-15'
        date_range = ["2020-11-25", "2020-12-15"]
        response = self.client.get(self.url)
        self.assertTrue(
            len(json.loads(response.content)) == Event.objects.filter(user__username=self.username,
                                                                      date__range=date_range).count())
        self.assertEqual(200, response.status_code)

    def test_get_events_invalid(self):
        self.test_event_create()
        response = self.client.get(self.url)
        self.assertEqual(400, response.status_code)

    def test_get_events_unauthorized(self):
        self.test_event_create()
        self.client.credentials()
        self.url += '?from=2020-11-25&to=2021-1-15'
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
