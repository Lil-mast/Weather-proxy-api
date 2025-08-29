from django.shortcuts import render

# Create your views here.
# weather/views.py

from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from .api import get_weather_data
from .serializers import WeatherResponseSerializer
from .api import get_weather_data, get_forecast_data 
from .serializers import WeatherResponseSerializer, ForecastDaySerializer

class CurrentWeatherView(APIView):
    """
    API view to get the current weather for a given location.
    """
    def get(self, request, *args, **kwargs):
        # 1. Parse and validate query parameters
        city = request.query_params.get('city')
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        # Ensure that either city or both lat/lon are provided
        if not city and not (lat and lon):
            return Response(
                {"error": "Please provide a location using 'city' or both 'lat' and 'lon' parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Call the API client to fetch data
        raw_data, error = get_weather_data(city=city, lat=lat, lon=lon)

        # 3. Handle any errors returned from the client
        if error:
            # Map client errors to the correct HTTP status codes
            if "not found" in error.lower():
                return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
            # Default to a service unavailable error for other issues
            return Response({"error": error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 4. Format the successful data using the serializer
        # This part transforms the complex raw_data into our simple, defined structure
        try:
            prepared_data = {
                'location': {
                    'city': raw_data['name'],
                    'country': raw_data['sys']['country']
                },
                'weather': {
                    'temperature_celsius': raw_data['main']['temp'],
                    'humidity_percent': raw_data['main']['humidity'],
                    'description': raw_data['weather'][0]['description'].capitalize()
                },
                'retrieved_at': datetime.now(timezone.utc),
                'source': 'live_api' # For now, it's always a live call
            }

            # Serialize the prepared data to ensure it matches our defined format
            serializer = WeatherResponseSerializer(data=prepared_data)
            serializer.is_valid(raise_exception=True) # This will raise an error if the data is malformed

            return Response(serializer.data, status=status.HTTP_200_OK)

        except (KeyError, IndexError) as e:
            # If the external API changes its format, we'll catch it here
            return Response(
                {"error": f"Failed to parse data from the external API: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WeatherDashboardView(TemplateView):
    """
    A view that renders the main weather dashboard HTML page.
    """
    template_name = 'weather/dashboard.html'

class ForecastWeatherView(APIView):
    """
    API view to get the 5-day weather forecast for a given location.
    """
    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city')
        # (Add lat/lon logic here if you need it)

        if not city:
            return Response({"error": "Please provide a 'city' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"forecast_{city.lower().replace(' ', '')}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        processed_forecast, error = get_forecast_data(city=city)

        if error:
            return Response({"error": error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        serializer = ForecastDaySerializer(data=processed_forecast, many=True)
        serializer.is_valid(raise_exception=True)

        cache.set(cache_key, serializer.data, timeout=3600) # Cache for 1 hour

        return Response(serializer.data, status=status.HTTP_200_OK)