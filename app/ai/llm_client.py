# ABOUTME: LLM API client for generating condition descriptions
# ABOUTME: Supports Google Gemini 2.5 Flash with fallback error handling

import google.generativeai as genai


class LLMClient:
    """Client for generating snarky descriptions via LLM API"""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_description(
        self,
        wind_speed: float,
        wind_direction: str,
        wave_height: float,
        swell_direction: str,
        rating: int,
        mode: str
    ) -> str:
        """
        Generate snarky description of conditions

        Args:
            wind_speed: Wind speed in knots
            wind_direction: Wind direction (N, S, E, W, etc.)
            wave_height: Wave height in feet
            swell_direction: Swell direction
            rating: 1-10 rating
            mode: "sup" or "parawing"

        Returns:
            1-2 paragraph snarky description
        """
        mode_name = "SUP foil" if mode == "sup" else "parawing"

        prompt = f"""You are an extremely passive-aggressive asshole giving a {mode_name} downwind rating to some dipshit checking if they should go out in Jupiter, FL.

CONDITIONS: {wind_speed}kts {wind_direction}, {wave_height}ft waves, {swell_direction} swell. Rating: {rating}/10.

Write 2-3 sentences MAX. Be viciously passive-aggressive. Question their skills and life choices. Use profanity including "cunt" and "fuck". You're giving THEM this rating - roast them directly."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM API error: {e}")
            return f"LLM service unavailable. Conditions: {wind_speed}kts {wind_direction}, {wave_height}ft waves. Rating: {rating}/10. Figure it out yourself."
