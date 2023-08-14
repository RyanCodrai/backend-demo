from fastapi import FastAPI
import logging
from weather import WeatherAPI


logging.basicConfig(
    filename='logs/weather_service.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


weather_api = WeatherAPI()
app = FastAPI(version='0.3.0')


def read_api_version():
    with open('VERSION') as f:
        return f.read()


@app.get("/ping/")
async def status():
    return {
      "name": "weatherservice",
      "status": "ok",
      "version": read_api_version()
    }


@app.get("/forecast/{city}/")
async def forecast(city):
    return weather_api.get_weather(city)
