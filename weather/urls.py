# weather/urls.py

from django.urls import path
from .views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    # This defines the final part of the URL: .../current/
    path('current/', CurrentWeatherView.as_view(), name='current-weather'),
    path('forecast/', ForecastWeatherView.as_view(), name='forecast-weather'),
]