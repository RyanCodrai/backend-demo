import os
from dotenv import load_dotenv
import requests
from fastapi import HTTPException

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
        response = requests.get(url, params=params).json()
        if len(response) == 0:
            raise HTTPException(status_code=404, detail=f'Cannot find city "{city}"')
        response_payload = response[0]
        return {
            'lat': response_payload['lat'],
            'lon': response_payload['lon']
        }


class WeatherAPI:
    def __init__(self):
        # Access api key stored in environment variable
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.geo_code_api = GeoCodeAPI()

    def get_weather(self, city, unix_time=None):
        url = f"https://api.openweathermap.org/data/3.0/onecall"

        lat_long = self.geo_code_api.get_lat_long(city)
        params = {
            'appid': self.api_key,
            'units': 'metric',
            **lat_long
        }
        if unix_time:
            params['dt'] = unix_time

        response = requests.get(url, params=params).json()
        response_payload = response['current']

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