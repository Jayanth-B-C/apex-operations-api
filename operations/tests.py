from django.test import TestCase
from rest_framework.test import APIClient

from .models import Operation


class OperationsAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_health_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)

    def test_health_response(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.json()['status'], 'healthy')

    def test_readiness_endpoint(self):
        response = self.client.get('/api/ready/')
        self.assertEqual(response.status_code, 200)

    def test_readiness_database(self):
        response = self.client.get('/api/ready/')
        self.assertEqual(response.json()['database'], 'connected')

    def test_operations_empty(self):
        response = self.client.get('/api/operations/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_create_and_list_operation(self):
        Operation.objects.create(
            name='Database Backup',
            description='Daily backup',
            status='COMPLETED'
        )

        response = self.client.get('/api/operations/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(
            response.json()['operations'][0]['name'],
            'Database Backup'
        )

    def test_metrics_endpoint(self):
        response = self.client.get('/api/metrics/')
        self.assertEqual(response.status_code, 200)