from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.core.cache import cache
from django.contrib.auth.models import User

from web.settings.base import REST_FRAMEWORK


class ApiTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user('dick', 'dick@dick.com', 'dickspassword')

    def tearDown(self):
        cache.clear()

    def test_anon_loads_root(self):
        client = APIClient()
        url = reverse('api:index')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anon_loads_concordance(self):
        client = APIClient()
        url = reverse('api:concordance')
        response = client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_anon_loads_segmentation(self):
        client = APIClient()
        url = reverse('api:segmentation')
        response = client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_anon_throttling(self):
        cache.clear()
        REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon'] = '2/min'
        client = APIClient()
        url = reverse('api:concordance')
        for i in range(0, 2):
            client.post(url, {'word': '台灣', 'page': i})

        response = client.post(url, {'word': '台灣'})
        self.assertEqual(response.status_code, 429)

    def test_user_throttling(self):
        cache.clear()
        REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['user'] = '3/min'
        client = APIClient()
        client.login(username='dick', password='dickspassword')
        url = reverse('api:concordance')
        for i in range(0, 2):
            client.post(url, {'word': '台灣', 'page': i})

        response = client.post(url, {'word': '台灣'})
        self.assertEqual(response.status_code, 200)
