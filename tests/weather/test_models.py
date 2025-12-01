# ABOUTME: Tests for weather data models and structures
# ABOUTME: Validates WeatherConditions data structure and defaults

from app.weather.models import WeatherConditions


def test_weather_conditions_creates_with_all_fields():
    """WeatherConditions should store all required fields"""
    conditions = WeatherConditions(
        wind_speed_kts=18.5,
        wind_direction="ESE",
        wave_height_ft=3.2,
        swell_direction="S",
        timestamp="2025-11-26T14:30:00"
    )

    assert conditions.wind_speed_kts == 18.5
    assert conditions.wind_direction == "ESE"
    assert conditions.wave_height_ft == 3.2
    assert conditions.swell_direction == "S"
    assert conditions.timestamp == "2025-11-26T14:30:00"


def test_weather_conditions_has_string_representation():
    """WeatherConditions should have readable string representation"""
    conditions = WeatherConditions(
        wind_speed_kts=18.5,
        wind_direction="ESE",
        wave_height_ft=3.2,
        swell_direction="S",
        timestamp="2025-11-26T14:30:00"
    )

    result = str(conditions)
    assert "18.5" in result
    assert "ESE" in result
    assert "3.2" in result
