# weather/api.py

import requests
from decouple import config

# Retrieve the API key from the .env file
OPENWEATHERMAP_API_KEY = config('OPENWEATHERMAP_API_KEY')
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city=None, lat=None, lon=None):
    """
    Fetches weather data from the OpenWeatherMap API for a given location.
    Can query by city name or by latitude and longitude.
    """
    params = {
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    # Add location parameters based on what's provided
    if city:
        params['q'] = city
    elif lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    else:
        # If no location is provided, we cannot proceed
        return None, "No location provided. Please specify a city or coordinates."

    try:
        # Make the GET request to the external API
        response = requests.get(WEATHER_API_URL, params=params)
        
        # This will raise an HTTPError if the HTTP request returned an unsuccessful status code (4xx or 5xx)
        response.raise_for_status()
        
        # If the request was successful, parse and return the JSON data
        return response.json(), None
        
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors, like 404 Not Found
        if response.status_code == 404:
            return None, f"Weather data not found for the specified location."
        return None, f"HTTP error occurred: {http_err}"
        
    except requests.exceptions.RequestException as req_err:
        # Handle other request-related errors (e.g., network issues)
        return None, f"An error occurred: {req_err}"