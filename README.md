Weather Proxy API

A Django-based backend API that consumes weather data from OpenWeatherMap, simplifies the response, and serves it through a clean, custom endpoint. This project acts as an intermediary to provide tailored weather data and reduce frontend dependency on external API changes.

About The Project

Tired of parsing complex and bloated responses from weather services? This Weather Proxy API is designed to solve that problem. It fetches rich data from the OpenWeatherMap API and transforms it into a simple, predictable JSON format focused on the most essential information: temperature, humidity, and a brief description.

This project is built as a capstone for the ALX Back-End Web Development program.

Core Features

Data Fetching: Retrieves current weather data by city name or geographic coordinates.

Data Simplification: Customizes and simplifies the returned JSON to be lightweight and user-friendly.

RESTful Endpoint: Provides a single, intuitive GET endpoint for all queries.

Robust Error Handling: Includes clear error messages for invalid inputs or external service failures.

Scalable Design: Built with a decoupled API client for easy maintenance and testing.

(Planned) Caching: Future implementation will include caching to reduce latency and external API calls.

API Usage

The API provides one primary endpoint for retrieving weather data.

Get Current Weather

Retrieves the simplified current weather for a specified location.

Endpoint: GET /api/weather/current/

Method: GET

Query Parameters

You must provide either a city or both lat and lon.

Parameter	Type	Description	Example
city	string	The name of the city.	?city=Nairobi
lat	float	The latitude of the location.	?lat=-1.2863
lon	float	The longitude of the location.	&lon=36.8172
Example Responses

✅ Success Response (200 OK)

Query: /api/weather/current/?city=London

code
JSON
download
content_copy
expand_less

{
  "location": {
    "city": "London",
    "country": "GB"
  },
  "weather": {
    "temperature_celsius": 15.7,
    "humidity_percent": 72,
    "description": "broken clouds"
  },
  "retrieved_at": "2025-08-24T14:10:00Z",
  "source": "live_api"
}

❌ Bad Request Response (400 Bad Request)

Query: /api/weather/current/ (no parameters)

code
JSON
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
{
  "error": "Please provide a location using 'city' or both 'lat' and 'lon' parameters."
}

❌ Not Found Response (404 Not Found)

Query: /api/weather/current/?city=InvalidCityName

code
JSON
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
{
  "error": "Weather data for the specified location could not be found."
}
Technology Stack

Python

Django

Django REST Framework

Requests

Python Decouple (for environment variable management)

Getting Started

Follow these instructions to get a local copy up and running for development and testing.

Prerequisites

Python 3.8+

An API key from OpenWeatherMap

