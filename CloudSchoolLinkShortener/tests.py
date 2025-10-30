import requests
from rest_framework import status
from rest_framework.test import APITestCase


class ShortenedURLUnitTests(APITestCase):
    def test_create_shortened_url_happy_path(self):
        url = 'https://example.com/some/long/path'
        response = self.client.post('/shrt/', {'original_url': url}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('hash', response.data)
        self.assertEqual(response.data['original_url'], url)

    def test_retrieve_nonexistent_hash_returns_404(self):
        non_existent_hash = 'nonexist'
        response = self.client.get(f'/shrt/{non_existent_hash}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ShortenedURLE2ETests(APITestCase):
    def test_shorten_and_redirect_real_google_humans_txt(self):
        google_humans_url = 'https://www.google.com/humans.txt'

        create_response = self.client.post(
            '/shrt/', {'original_url': google_humans_url}, format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        real_response = requests.get(google_humans_url)
        self.assertEqual(real_response.status_code, 200)
        self.assertIn('Google is built by a large team', real_response.text)
