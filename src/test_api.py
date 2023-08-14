import unittest
import requests
from dotenv import load_dotenv
import os
from utils import read_api_version, iso_to_unix

# Load environment variables from .env file
load_dotenv()


class TestWeatherService(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources before each test case
        self.base_url = "http://localhost:8080"
        self.api_version = read_api_version()
        # Access api key stored in environment variable
        self.api_key = os.getenv("WEATHER_API_KEY")

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


    def test_city_weather_time(self):
        # Test weather for London at a specific date and time
        error_message = f"Service did not respond with correct weather information"

        city_name = 'London'
        iso_time = '2018-10-14T14:34:40+0100'
        unix_time = iso_to_unix(iso_time)

        url = f"https://api.openweathermap.org/data/3.0/onecall?lat=51.5073219&lon=-0.1276474&units=metric&dt={unix_time}&appid={self.api_key}"
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

        params = {'at': iso_time}
        api_response = requests.get(f'{self.base_url}/forecast/{city_name}/', params=params).json()
        self.assertEqual(api_response, ideal_response, error_message)

    def test_city_not_found(self):
        # Test the current weather for a made up city that can't be found
        error_message = f"Service did not respond 404 for city not found"
        city_name = 'midgar'
        api_response = requests.get(f'{self.base_url}/forecast/{city_name}/')
        self.assertEqual(api_response.status_code, 404, error_message)

    def test_short_date(self):
        # Test whether the api correctly responds with 400 for date before January 1st, 1970.
        error_message = f"Service did not respond 400 for date before January 1st, 1970."
        city_name = 'London'
        iso_time = '2020-12-25'
        api_response = requests.get(f'{self.base_url}/forecast/{city_name}', params={'at': iso_time})
        self.assertEqual(api_response.status_code, 400, error_message)

    def test_date_in_past(self):
        # Test whether the api correctly responds with 400 for date before January 1st, 1970.
        error_message = f"Service did not respond 400 for date before January 1st, 1970."
        city_name = 'London'
        iso_time = '1938-12-25'
        api_response = requests.get(f'{self.base_url}/forecast/{city_name}', params={'at': iso_time})
        self.assertEqual(api_response.status_code, 400, error_message)

    def test_date_in_future(self):
        # Test whether the api correctly responds with 400 for date in the future
        error_message = f"Service did not respond 400 for date in the future"
        city_name = 'London'
        iso_time = '2025-01-01'
        api_response = requests.get(f'{self.base_url}/forecast/{city_name}', params={'at': iso_time})
        self.assertEqual(api_response.status_code, 400, error_message)





if __name__ == '__main__':
    unittest.main()
