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


class UpdateDeleteEventTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateDeleteEventTestCase, self).setUp()

        self.event = Event.objects.create(title='My title', date='2020-11-26 19:33', content='test description',
                                          user=self.user)
        self.user_2 = User.objects.create_user(username='test@mail.com', email='test@mail.com',
                                               password='password5353')
        self.url += f"{self.event.uuid}"

        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="selamet@mail.com", password="qwe123123"):
        response = self.client.post(self.login_url, data={'username': username, 'password': password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_update_event_patch(self):
        response = self.client.patch(self.url, data={'title': 'title update', 'date': '2020-11-26 19:33'})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Event.objects.get(uuid=self.event.uuid).title, "title update")

    def test_update_event_put(self):
        response = self.client.put(self.url, data={'title': 'title update', 'date': '2020-11-26 19:33'})
        self.assertEqual(405, response.status_code)

    def test_update_event_patch_other_user(self):
        self.test_jwt_authentication(username="test@mail.com", password='password5353')
        response = self.client.patch(self.url, data={'title': 'title update', 'date': '2020-11-26 19:33'})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Event.objects.get(uuid=self.event.uuid).content, "title update")

    def test_update_event_invalid(self):
        self.url += '1'
        response = self.client.patch(self.url, data={'title': 'title update', 'date': '2020-11-26 19:33'})
        self.assertEqual(404, response.status_code)

    def test_delete_event(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Event.objects.filter(uuid=self.event.uuid).exists())

    def test_delete_event_other_user(self):
        self.test_jwt_authentication(username="test@mail.com", password='password5353')
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_delete_event_unauthorized(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        self.assertEqual(401, response.status_code)
