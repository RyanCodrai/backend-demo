# Weather API

## Installation
1. Install docker and docker-compose
2. Create a file named `.env` in the `src` directory.
3. Add `WEATHER_API_KEY={api_key}` to a `.env` using your open weather api key.
4. Run `docker-compose up -d` to launch the docker container

## Running the unit tests
1. Run `cd src` to navigate into the `src` directory.
2. Run `python3 test_api.py`.

## Swagger documentation
Navigate to http://localhost:8080/docs once the container has been started to find documentation on the weather API endpoints.
