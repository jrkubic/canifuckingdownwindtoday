# ABOUTME: Debug logging utilities
# ABOUTME: Provides conditional logging when DEBUG=true

from app.config import Config


def debug_log(message: str, category: str = "DEBUG") -> None:
    """
    Print debug message if DEBUG mode is enabled.

    Args:
        message: The message to log
        category: Category prefix (e.g., "CACHE", "LLM", "WEATHER")
    """
    if Config.DEBUG:
        print(f"[{category}] {message}")
