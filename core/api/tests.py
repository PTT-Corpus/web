from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient


class ApiTests(APITestCase):
    TESTING_THRESHOLD = '5/min'

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
        client = APIClient()
        url = reverse('api:concordance')
        for i in range(0, 2):
            client.post(url, {'word': '台灣'})

        response = client.post(url, {'word': '台灣'})
        self.assertEqual(response.status_code, 429)
