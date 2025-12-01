# ABOUTME: Tests for application configuration and location settings
# ABOUTME: Validates Jupiter FL coordinates and weather API configuration

from app.config import Config


def test_config_has_jupiter_coordinates():
    """Jupiter, FL coordinates should be defined"""
    assert Config.LOCATION_LAT == 26.9
    assert Config.LOCATION_LON == -80.1


def test_config_has_location_name():
    """Location name should be Jupiter FL"""
    assert Config.LOCATION_NAME == "Jupiter, FL"


def test_config_has_cache_refresh_hours():
    """Cache refresh interval should be configurable"""
    assert Config.CACHE_REFRESH_HOURS >= 1
    assert Config.CACHE_REFRESH_HOURS <= 24
