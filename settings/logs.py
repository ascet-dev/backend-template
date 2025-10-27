from adc_logger import BaseLoggingConfig
from adc_logger.configs import LoggerConfig
from pydantic import Field
from pydantic_settings import BaseSettings

from .env import ENV
from .sentry import Sentry


class LoggingConfig(BaseLoggingConfig):
    default_handlers = ["console_generic"] if ENV == "LOCAL" else ["console_json"]
    access_handler = ["console_access"] if ENV == "LOCAL" else ["console_json"]

    loggers = [
        LoggerConfig("", handlers=default_handlers),
        LoggerConfig("root", handlers=default_handlers, level="DEBUG", propagate=False),
        LoggerConfig("envparse", handlers=default_handlers, level="ERROR"),
        LoggerConfig("uvicorn", handlers=default_handlers, level="INFO", propagate=False),
        LoggerConfig("uvicorn.error", handlers=default_handlers, level="INFO", propagate=False),
        LoggerConfig("uvicorn.access", handlers=access_handler, level="INFO", propagate=False),
        LoggerConfig("botocore", handlers=default_handlers, level="ERROR"),
        LoggerConfig("aiocache", handlers=default_handlers, level="ERROR"),
        LoggerConfig("multipart", handlers=default_handlers, level="ERROR"),
    ]


class Logging(BaseSettings):
    log_level: str = "DEBUG"
    unlog_path: list[str] = Field(default_factory=lambda: ["/readiness", "/liveness", "/metrics"])
    access_log: bool = True
    config: LoggingConfig = Field(default_factory=LoggingConfig)
    sentry: Sentry = Field(default_factory=Sentry)
