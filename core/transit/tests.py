from django.test import TestCase, Client

# Create your tests here.

class TestTransit(TestCase):

    def test_index(self):
        c = Client()

        response = c.get("")

        self.assertEqual(response.status_code, 200)