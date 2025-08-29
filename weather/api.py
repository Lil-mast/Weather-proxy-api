# weather/api.py

import requests
from decouple import config
from datetime import datetime

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

FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_forecast_data(city=None, lat=None, lon=None):
    """
    Fetches 5-day weather forecast data from OpenWeatherMap and processes it
    to return a simplified list of daily forecasts.
    """
    params = {
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric'
    }
    if city:
        params['q'] = city
    elif lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    else:
        return None, "No location provided."

    try:
        response = requests.get(FORECAST_API_URL, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
        # --- Process the raw forecast data into a daily summary ---
        daily_forecasts = {}
        for forecast in raw_data['list']:
            date = datetime.fromtimestamp(forecast['dt']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temps': [],
                    'descriptions': {},
                    'icons': {}
                }
            daily_forecasts[date]['temps'].append(forecast['main']['temp'])
            
            # Count descriptions and icons to find the most common one for the day
            desc = forecast['weather'][0]['description'].capitalize()
            icon = forecast['weather'][0]['icon']
            daily_forecasts[date]['descriptions'][desc] = daily_forecasts[date]['descriptions'].get(desc, 0) + 1
            daily_forecasts[date]['icons'][icon] = daily_forecasts[date]['icons'].get(icon, 0) + 1

        processed_forecast = []
        for date, data in sorted(daily_forecasts.items()):
            if not data['temps']: continue # Skip if no data
            
            processed_forecast.append({
                'date': date.isoformat(),
                'day_of_week': date.strftime('%A'),
                'temp_high': max(data['temps']),
                'temp_low': min(data['temps']),
                'description': max(data['descriptions'], key=data['descriptions'].get),
                'icon_url': f"http://openweathermap.org/img/wn/{max(data['icons'], key=data['icons'].get)}@2x.png"
            })
        
        # We only need the next 5 days, starting from tomorrow
        return processed_forecast[1:6], None

    except requests.exceptions.HTTPError as http_err:
        return None, f"HTTP error occurred: {http_err}"
    except Exception as err:
        return None, f"An error occurred during forecast processing: {err}"