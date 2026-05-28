from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value is None else int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value is None else float(value)


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    ui_base_url: str
    api_base_url: str
    default_timeout_ms: int
    api_timeout_seconds: float
    swag_labs_standard_username: str
    swag_labs_password: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached framework settings for the current test process."""

    return Settings(
        ui_base_url=os.getenv("UI_BASE_URL", "https://www.saucedemo.com/"),
        api_base_url=os.getenv(
            "API_BASE_URL",
            "https://jsonplaceholder.typicode.com/",
        ),
        default_timeout_ms=_get_int("DEFAULT_TIMEOUT_MS", 10_000),
        api_timeout_seconds=_get_float("API_TIMEOUT_SECONDS", 10.0),
        swag_labs_standard_username=os.getenv(
            "SWAG_LABS_STANDARD_USERNAME",
            "standard_user",
        ),
        swag_labs_password=os.getenv("SWAG_LABS_PASSWORD", "secret_sauce"),
    )
