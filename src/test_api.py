import unittest
import requests


class TestLocalService(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources before each test case
        self.base_url = "http://localhost:8080"

    def test_availability(self):
        # Test if the service responds with a successful status code
        error_message = "Service did not respond with a 200 status code"
        ideal_response = {
          "name": "weatherservice",
          "status": "ok",
          "version": "1.0.0"
        }

        api_response = requests.get(f'{self.base_url}/ping')
        self.assertEqual(api_response.json(), ideal_response, error_message)

if __name__ == '__main__':
    unittest.main()
