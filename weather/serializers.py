# weather/serializers.py

from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    """Serializer for location data."""
    city = serializers.CharField()
    country = serializers.CharField()

class WeatherDataSerializer(serializers.Serializer):
    """Serializer for the main weather data points."""
    temperature_celsius = serializers.FloatField()
    humidity_percent = serializers.IntegerField()
    description = serializers.CharField()
    # --- ADD THE NEW FIELDS HERE ---
    temp_high_celsius = serializers.FloatField()
    temp_low_celsius = serializers.FloatField()
    wind_speed_ms = serializers.FloatField() 

class WeatherResponseSerializer(serializers.Serializer):
    """Top-level serializer for the final API response."""
    location = LocationSerializer()
    weather = WeatherDataSerializer()
    retrieved_at = serializers.DateTimeField()
    source = serializers.CharField()

class ForecastDaySerializer(serializers.Serializer):
    """Serializer for a single day's forecast summary."""
    date = serializers.DateField()
    day_of_week = serializers.CharField()
    temp_high = serializers.FloatField()
    temp_low = serializers.FloatField()
    description = serializers.CharField()
    icon_url = serializers.URLField()