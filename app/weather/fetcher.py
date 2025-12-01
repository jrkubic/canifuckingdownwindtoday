# ABOUTME: Orchestrates weather data fetching from multiple sources
# ABOUTME: Handles primary/fallback API logic and error recovery

from typing import Optional
from app.weather.sources import NOAAClient
from app.weather.models import WeatherConditions


class WeatherFetcher:
    """Orchestrates weather data fetching from multiple sources"""

    def __init__(self):
        self.noaa_client = NOAAClient()

    def fetch_current_conditions(self, lat: float, lon: float) -> Optional[WeatherConditions]:
        """
        Fetch current weather conditions for given coordinates

        Tries NOAA first, falls back to other sources if needed

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            WeatherConditions or None if all sources fail
        """
        try:
            return self.noaa_client.fetch_conditions(lat, lon)
        except Exception as e:
            print(f"NOAA fetch failed: {e}")
            # TODO: Add fallback sources (OpenWeatherMap, etc.)
            return None
