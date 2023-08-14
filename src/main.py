from fastapi import FastAPI, HTTPException
import logging
from weather import WeatherAPI
from utils import read_api_version, iso_to_unix
import time


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


@app.get("/ping/")
async def status():
    return {
      "name": "weatherservice",
      "status": "ok",
      "version": read_api_version()
    }


@app.get("/forecast/{city}/")
async def forecast(city, at=None):
    unix_time = iso_to_unix(at) if at else int(time.time())
    if unix_time and unix_time < 0:
        raise HTTPException(
            status_code=400,
            detail=f'No data available for "{at}" as datetime is before January 1st, 1970.'
        )
    if unix_time and unix_time > time.time():
        raise HTTPException(
            status_code=400,
            detail=f'No data available for "{at}" as datetime is in the future.'
        )
    return weather_api.get_weather(city, unix_time)
