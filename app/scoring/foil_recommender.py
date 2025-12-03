# ABOUTME: Foil setup recommendations based on conditions and score
# ABOUTME: Provides CODE and KT Atlas equipment suggestions matched to condition tiers

from typing import Optional
from app.weather.models import WeatherConditions


class FoilRecommender:
    """
    Recommends foil setups based on conditions.

    Score tiers:
    - 1-4: Light/marginal conditions
    - 5-7: Good/decent conditions
    - 8-10: Great conditions / big swell

    Note: Recommendations calibrated for 195lb/88kg rider.
    """

    # CODE Foil recommendations by tier
    CODE_SETUPS = {
        "light": "1250R + 135R stab + short fuse",
        "good": "960R + 135R stab + short fuse",
        "great": "770R + 135R stab + short fuse"
    }

    # KT Atlas equivalents (sized down 10-20% per KT recommendation)
    KT_SETUPS = {
        "light": "Atlas 1130 + 145 Paka'a + 56cm fuse",
        "good": "Atlas 790 or 960 + 145 Paka'a + 56cm fuse",
        "great": "Atlas 680 + 170 Paka'a + 56cm fuse"
    }

    def _score_to_tier(self, score: int) -> str:
        """Convert 1-10 score to condition tier"""
        if score <= 4:
            return "light"
        elif score <= 7:
            return "good"
        else:
            return "great"

    def _conditions_to_score(self, conditions: WeatherConditions) -> int:
        """Estimate score from conditions for backwards compatibility"""
        # Simple heuristic matching old behavior
        if conditions.wind_speed_kts < 15 and conditions.wave_height_ft < 2.5:
            return 3  # Light
        elif conditions.wind_speed_kts >= 20 and conditions.wave_height_ft >= 3:
            return 8  # Great
        else:
            return 6  # Good

    def recommend_code(
        self,
        score: Optional[int] = None,
        conditions: Optional[WeatherConditions] = None
    ) -> str:
        """
        Recommend CODE foil setup based on score or conditions.

        Args:
            score: 1-10 rating (preferred)
            conditions: WeatherConditions (for backwards compat)

        Returns:
            Setup string (e.g., "960R + 135R stab + short fuse")
        """
        if score is None and conditions is not None:
            score = self._conditions_to_score(conditions)
        elif score is None:
            raise ValueError("Must provide either score or conditions")

        tier = self._score_to_tier(score)
        return self.CODE_SETUPS[tier]

    def recommend_kt(
        self,
        score: Optional[int] = None,
        conditions: Optional[WeatherConditions] = None
    ) -> str:
        """
        Recommend KT Atlas setup based on score or conditions.

        Args:
            score: 1-10 rating (preferred)
            conditions: WeatherConditions (for backwards compat)

        Returns:
            Setup string (e.g., "Atlas 790 or 960 + 145 Paka'a + 56cm fuse")
        """
        if score is None and conditions is not None:
            score = self._conditions_to_score(conditions)
        elif score is None:
            raise ValueError("Must provide either score or conditions")

        tier = self._score_to_tier(score)
        return self.KT_SETUPS[tier]
