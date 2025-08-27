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

class WeatherResponseSerializer(serializers.Serializer):
    """Top-level serializer for the final API response."""
    location = LocationSerializer()
    weather = WeatherDataSerializer()
    retrieved_at = serializers.DateTimeField()
    source = serializers.CharField()