import logging
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


class Sentry(BaseSettings):
    enabled: bool = False
    dsn: str | None = None
    integrations: list[Any] = Field(
        default_factory=lambda: [
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            StarletteIntegration(),
        ],
    )
