from django.test import TestCase, Client

# Create your tests here.

class TestTransit(TestCase):

    def test_index(self):
        c = Client()

        response = c.get("")

        self.assertEqual(response.status_code, 200)
    
    def test_dashboard(self):
        c = Client()

        response = c.get("dashboard")
        self.assertEqual(response.status_code, 404)

    def test_driver_dashboard(self):
        c = Client()

        response = c.get("driver/dashboard")
        self.assertEqual(response.status_code, 404)