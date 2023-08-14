import unittest
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class TestWeatherService(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources before each test case
        self.base_url = "http://localhost:8080"
        self.api_version = self.read_api_version()
        # Access api key stored in environment variable
        self.api_key = os.getenv("WEATHER_API_KEY")

    @staticmethod
    def read_api_version():
        with open('VERSION') as f:
            return f.read()

    @staticmethod
    def cloud_cover_description(cloud_percentage):
        if cloud_percentage < 11:
            return 'clear sky'
        elif cloud_percentage < 25:
            return 'few clouds'
        elif cloud_percentage < 51:
            return 'scattered clouds'
        elif cloud_percentage < 85:
            return 'broken clouds'
        else:
            return 'overcast clouds'

    def test_availability(self):
        # Test if the service responds with the correct status information
        error_message = "Service did not respond with correct status information"
        ideal_response = {
          "name": "weatherservice",
          "status": "ok",
          "version": self.api_version
        }

        api_response = requests.get(f'{self.base_url}/ping/')
        self.assertEqual(api_response.json(), ideal_response, error_message)

    def test_city_weather(self):
        # Test the current weather for London
        error_message = f"Service did not respond with correct weather information"

        city_name = 'London'
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat=51.5073219&lon=-0.1276474&units=metric&appid={self.api_key}"
        response = requests.get(url)
        response_payload = response.json()['current']

        cloud_cover = None
        for weather in response_payload['weather']:
            if weather['main'] == 'Clouds':
                cloud_cover = weather['description']

        ideal_response = {
            'temperature': f'{response_payload["temp"]}C',
            'humidity': f'{response_payload["humidity"]}%',
            'pressure': f'{response_payload["pressure"]} hPa',
            'clouds': cloud_cover
        }

        api_response = requests.get(f'{self.base_url}/forecast/{city_name}/').json()
        self.assertEqual(api_response, ideal_response, error_message)


if __name__ == '__main__':
    unittest.main()
