# ABOUTME: Tests for weather fetcher orchestration logic
# ABOUTME: Validates combining multiple API sources and fallback behavior

from unittest.mock import Mock, patch
from app.weather.fetcher import WeatherFetcher
from app.weather.models import WeatherConditions


def test_weather_fetcher_uses_noaa_as_primary():
    """WeatherFetcher should try NOAA first"""
    mock_conditions = WeatherConditions(
        wind_speed_kts=18.0,
        wind_direction="ESE",
        wave_height_ft=3.0,
        swell_direction="S",
        timestamp="2025-11-26T14:30:00"
    )

    with patch('app.weather.fetcher.NOAAClient') as mock_noaa:
        mock_noaa.return_value.fetch_conditions.return_value = mock_conditions

        fetcher = WeatherFetcher()
        result = fetcher.fetch_current_conditions(26.9, -80.1)

        assert result == mock_conditions
        mock_noaa.return_value.fetch_conditions.assert_called_once_with(26.9, -80.1)


def test_weather_fetcher_handles_noaa_failure():
    """WeatherFetcher should handle NOAA API failures gracefully"""
    with patch('app.weather.fetcher.NOAAClient') as mock_noaa:
        mock_noaa.return_value.fetch_conditions.side_effect = Exception("NOAA API down")

        fetcher = WeatherFetcher()
        result = fetcher.fetch_current_conditions(26.9, -80.1)

        # Should return None on failure (we'll add fallback sources later)
        assert result is None
