from django.test import TestCase
from rest_framework.test import APIClient


class IntentionalFailureDemo(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_intentional_failure_example(self):
        response = self.client.get('/api/health/')

        # Deliberately incorrect expectation.
        self.assertEqual(response.status_code, 201)