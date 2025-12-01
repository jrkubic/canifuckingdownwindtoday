# ABOUTME: Data models for weather conditions and forecasts
# ABOUTME: Provides structured representation of wind, waves, and swell data

from dataclasses import dataclass


@dataclass
class WeatherConditions:
    """Raw weather conditions from APIs"""
    wind_speed_kts: float
    wind_direction: str
    wave_height_ft: float
    swell_direction: str
    timestamp: str

    def __str__(self) -> str:
        return (
            f"Wind: {self.wind_speed_kts}kts {self.wind_direction}, "
            f"Waves: {self.wave_height_ft}ft, "
            f"Swell: {self.swell_direction}"
        )
