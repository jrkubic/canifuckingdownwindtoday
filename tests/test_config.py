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


def test_config_has_correct_wind_directions_for_jupiter():
    """
    Jupiter FL coast runs N-S, so optimal wind follows the coast.
    Best: N, S (parallel to coast - pushes along the run)
    Good: NE, SE, NW, SW (diagonal - has component along coast)
    Bad: E, W (perpendicular - pushes into shore or out to sea)
    """
    # Best directions should be N and S
    assert "N" in Config.OPTIMAL_WIND_DIRECTIONS
    assert "S" in Config.OPTIMAL_WIND_DIRECTIONS

    # Good directions should include diagonals
    assert "NE" in Config.GOOD_WIND_DIRECTIONS
    assert "SE" in Config.GOOD_WIND_DIRECTIONS
    assert "NW" in Config.GOOD_WIND_DIRECTIONS
    assert "SW" in Config.GOOD_WIND_DIRECTIONS

    # Bad directions should NOT be in optimal or good
    assert "E" not in Config.OPTIMAL_WIND_DIRECTIONS
    assert "W" not in Config.OPTIMAL_WIND_DIRECTIONS
    assert "E" not in Config.GOOD_WIND_DIRECTIONS
    assert "W" not in Config.GOOD_WIND_DIRECTIONS

    # Bad directions should be explicitly listed
    assert "E" in Config.BAD_WIND_DIRECTIONS
    assert "W" in Config.BAD_WIND_DIRECTIONS
