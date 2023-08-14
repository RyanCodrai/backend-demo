import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()


class GeoCodeAPI:
    def __init__(self):
        # Access api key stored in environment variable
        self.api_key = os.getenv("WEATHER_API_KEY")

    def get_lat_long(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
        }
        url = f"http://api.openweathermap.org/geo/1.0/direct"
        response = requests.get(url, params=params)
        response_payload = response.json()[0]
        return {
            'lat': response_payload['lat'],
            'lon': response_payload['lon']
        }


class WeatherAPI:
    def __init__(self):
        # Access api key stored in environment variable
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.geo_code_api = GeoCodeAPI()

    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/3.0/onecall"

        lat_long = self.geo_code_api.get_lat_long(city)
        params = {'appid': self.api_key, **lat_long}

        response = requests.get(url, params=params)
        response_payload = response.json()['current']

        cloud_cover = None
        for weather in response_payload['weather']:
            if weather['main'] == 'Clouds':
                cloud_cover = weather['description']

        return {
            'temperature': f'{response_payload["temp"]}C',
            'humidity': f'{response_payload["humidity"]}%',
            'pressure': f'{response_payload["pressure"]} hPa',
            'clouds': cloud_cover
        }


api = WeatherAPI()
print(api.get_weather('London'))