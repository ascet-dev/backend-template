from pydantic_settings import BaseSettings


class Doc(BaseSettings):
    title: str = "AppName"
    version: str = "0.1.0"
    route: str = "/doc.json"
    schemes: list[str] = ["http", "https"]
