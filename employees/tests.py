from django.test import TestCase, Client

class PingTest(TestCase):
    def test_ping(self):
        client = Client()
        response = client.get('/ping/')
        self.assertEqual(response.status_code, 200)